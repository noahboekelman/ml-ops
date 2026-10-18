import json
import os
from typing import Literal
from uuid import uuid4

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from numpy.random import random

from app.config import get_config
from app.dashboard import dashboard_html_str
from app.models import (
    PatientPrediction,
    PredictionRequest,
    PredictionResponse,
    PredictionsResponse,
)

app = FastAPI()

config = get_config()

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
    #try:
    #    
    #except Exception as e:
    #   raise HTTPException(status_code=500, detail=f"Prediction failed with message: {str(e)}") from e
    # pyrefly: ignore[missing-argument]
    # TODO: Change when model is built, just for CI for now
    placeholder_prediction = random()
    nurse_id = request.nurse_id
    patient_id = request.patient_id
    patient_values = request.model_dump(exclude={"patient_id", "nurse_id"})
    
    # Save to JSON file
    write_patient_prediction(
        nurse_id=nurse_id,
        patient_id=patient_id,
        prediction=placeholder_prediction,
        patient_values=patient_values
    )
    
    return PredictionResponse(prediction=placeholder_prediction)

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
