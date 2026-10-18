from pydantic import BaseModel


class PredictionRequest(BaseModel):
    "Validation happens here, and the model is used in the API contract"
    
    nurse_id: str
    patient_id: str
    age: float
    sex: float
    bmi: float
    bp: float
    s1: float
    s2: float
    s3: float
    s4: float
    s5: float
    s6: float
    
class PredictionResponse(BaseModel):
    "The prediction returned by the model"
    
    prediction: float
    
class PatientInputValues(BaseModel):
    age: float
    sex: float
    bmi: float
    bp: float
    s1: float
    s2: float
    s3: float
    s4: float
    s5: float
    s6: float
    
class PatientPrediction(BaseModel):
    id: str
    prediction: float
    patient_input_values: PatientInputValues
    
class PredictionsResponse(BaseModel):
    predictions: list[PatientPrediction]