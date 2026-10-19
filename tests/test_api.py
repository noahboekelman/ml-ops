from fastapi.testclient import TestClient

from app.config import get_config
from app.main import app

client = TestClient(app)

VALID_PAYLOAD = {
    "nurse_id": "nurse-test",
    "patient_id": "patient-test",
    "age": 0.02,
    "sex": -0.044,
    "bmi": 0.06,
    "bp": -0.03,
    "s1": -0.02,
    "s2": 0.03,
    "s3": -0.02,
    "s4": 0.02,
    "s5": 0.02,
    "s6": -0.001,
}


def test_health_returns_ok_and_version():
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["model_version"] == get_config().model_version


def test_predict_returns_numeric_prediction():
    response = client.post("/predict", json=VALID_PAYLOAD)
    assert response.status_code == 200
    body = response.json()
    assert isinstance(body["prediction"], float)


def test_dashboard_predict_missing_ids_returns_422():
    payload = {"values": {k: v for k, v in VALID_PAYLOAD.items() if k not in {"nurse_id", "patient_id"}}}
    response = client.post("/dashboard/predict", json=payload)
    assert response.status_code == 422
    body = response.json()
    assert "detail" in body


def test_predict_missing_feature_returns_422():
    payload = VALID_PAYLOAD.copy()
    del payload["s6"]
    response = client.post("/predict", json=payload)
    assert response.status_code == 422
    body = response.json()
    assert "detail" in body
