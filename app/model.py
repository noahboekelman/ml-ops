import json
from pathlib import Path
from typing import cast

import joblib
import pandas as pd
from sklearn.datasets import load_diabetes
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.metrics import precision_score, recall_score, root_mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from app.config import get_config

RANDOM_STATE = 0
TEST_SIZE = 0.2
RIDGE_ALPHA = 10.0
HIGH_RISK_QUANTILE = 0.75

FEATURE_NAMES = ["age", "sex", "bmi", "bp", "s1", "s2", "s3", "s4", "s5", "s6"]

MODEL_STORE_DIR = Path(__file__).resolve().parent / "model_store"
MODEL_PATH = MODEL_STORE_DIR / "model.joblib"
METRICS_PATH = MODEL_STORE_DIR / "metrics.json"


def load_dataset() -> tuple[pd.DataFrame, pd.Series]:
    X, y = cast(
        tuple[pd.DataFrame, pd.Series],
        load_diabetes(as_frame=True, return_X_y=True),
    )
    return X, y


def build_pipeline(model_version: str) -> Pipeline:
    if model_version == "v0.2":
        regressor = Ridge(alpha=RIDGE_ALPHA)
    else:
        regressor = LinearRegression()
    return Pipeline([("scaler", StandardScaler()), ("regressor", regressor)])


def train() -> dict:
    model_version = get_config().model_version
    X, y = load_dataset()
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE
    )
    pipeline = build_pipeline(model_version)
    pipeline.fit(X_train, y_train)
    predictions = cast(pd.Series, pipeline.predict(X_test))
    rmse = float(root_mean_squared_error(y_test, predictions))

    threshold = float(y_train.quantile(HIGH_RISK_QUANTILE))
    true_high_risk = (y_test >= threshold).astype(int)
    predicted_high_risk = (predictions >= threshold).astype(int)
    precision = float(precision_score(true_high_risk, predicted_high_risk, zero_division=0))
    recall = float(recall_score(true_high_risk, predicted_high_risk, zero_division=0))

    MODEL_STORE_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, MODEL_PATH)
    metrics = {
        "model_version": model_version,
        "estimator": type(pipeline.named_steps["regressor"]).__name__,
        "rmse": rmse,
        "high_risk_threshold": threshold,
        "high_risk_quantile": HIGH_RISK_QUANTILE,
        "precision": precision,
        "recall": recall,
        "n_train": int(X_train.shape[0]),
        "n_test": int(X_test.shape[0]),
        "random_state": RANDOM_STATE,
        "test_size": TEST_SIZE,
    }
    METRICS_PATH.write_text(json.dumps(metrics, indent=2))
    return metrics


def load_model() -> Pipeline:
    return joblib.load(MODEL_PATH)


def main() -> None:
    metrics = train()
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
