import json
import os
from functools import lru_cache
from typing import Literal
from uuid import uuid4

import pandas as pd
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from app.config import get_config
from app.dashboard import dashboard_html_str
from app.model import FEATURE_NAMES, load_model
from app.models import (
    PatientPrediction,
    PredictionRequest,
    PredictionResponse,
    PredictionsResponse,
)

app = FastAPI()

config = get_config()


@lru_cache
def get_model():
    return load_model()

_RECORDS_PATH = "./app/data/records.json"

def write_patient_prediction(nurse_id: str, patient_id: str, prediction: float, patient_values: dict) -> None:
    """Stand-in database operations, as creating a database was out of scope for this assignment.
    We still need to store the nurse's patient predictions for the dashboard though.
    This data will not survive Docker runs, but will survive local API runs.
    """
    new_patient = {"nurse_id": nurse_id, "patient_id": patient_id, "prediction": prediction, "patient_input_values": patient_values}

    if os.path.exists(_RECORDS_PATH):
        with open(_RECORDS_PATH) as file:
            data = json.load(file)
    else:
        # Handle first time write
        data = {"patients": []}

    data["patients"].append(new_patient)

    # Create app/data/records.json
    os.makedirs(os.path.dirname(_RECORDS_PATH), exist_ok=True)
    with open(_RECORDS_PATH, "w") as file:
        json.dump(data, file, indent=4)

@app.get("/health")
async def health() -> dict:
    return {"status":"ok", "model_version": config.model_version}


@app.post("/predict")
async def predict(request: PredictionRequest) -> PredictionResponse:
    patient_values = request.model_dump(exclude={"patient_id", "nurse_id"})
    features = pd.DataFrame(
        [[patient_values[name] for name in FEATURE_NAMES]], columns=FEATURE_NAMES
    )
    prediction = float(get_model().predict(features)[0])

    write_patient_prediction(
        nurse_id=request.nurse_id,
        patient_id=request.patient_id,
        prediction=prediction,
        patient_values=patient_values,
    )

    return PredictionResponse(prediction=prediction)

@app.get("/generate-nurse-id")
async def generate_nurse_id() -> str:
    "Generates a one-time nurse id to group each patient prediction per nurse."
    return str(uuid4())

@app.get("/nurse/{nurse_id}/patients")
def get_nurse_patients(nurse_id: str, sorting_order: Literal["ascending", "descending"] = "descending") -> PredictionsResponse:
    if not os.path.exists(_RECORDS_PATH):
        return PredictionsResponse(predictions=[])

    with open(_RECORDS_PATH) as file:
        data = json.load(file)
        nurse_patients = [PatientPrediction(id=p["patient_id"], prediction=p["prediction"], patient_input_values=p["patient_input_values"]) for p in data["patients"] if p["nurse_id"] == nurse_id]
        nurse_patients.sort(key=lambda p: p.prediction, reverse=sorting_order == "descending")
    return PredictionsResponse(predictions=nurse_patients)

@app.get("/")
async def main():
    return HTMLResponse(content=dashboard_html_str, status_code=200)

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard() -> HTMLResponse:
    return HTMLResponse(content=dashboard_html_str, status_code=200)
