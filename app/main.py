from fastapi import FastAPI, HTTPException

from app.config import get_config
from app.models import PredictionRequest, PredictionResponse

app = FastAPI()

config = get_config()

@app.get("/health")
async def health() -> dict:
    return {"status":"ok", "model_version": config.model_version}


@app.post("/predict")
async def predict(request: PredictionRequest) -> PredictionResponse:
    # TODO: Change when model is built
    #try:
    #    
    #except Exception as e:
    #   raise HTTPException(status_code=500, detail=f"Prediction failed with message: {str(e)}") from e
    return PredictionResponse()