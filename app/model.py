import json
from pathlib import Path
from typing import cast

import joblib
import pandas as pd
from sklearn.datasets import load_diabetes
from sklearn.linear_model import LinearRegression
from sklearn.metrics import root_mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from app.config import get_config

RANDOM_STATE = 0
TEST_SIZE = 0.2

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


def build_pipeline() -> Pipeline:
    return Pipeline(
        [("scaler", StandardScaler()), ("regressor", LinearRegression())]
    )


def train() -> dict:
    model_version = get_config().model_version
    X, y = load_dataset()
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE
    )
    pipeline = build_pipeline()
    pipeline.fit(X_train, y_train)
    rmse = float(root_mean_squared_error(y_test, pipeline.predict(X_test)))
    MODEL_STORE_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, MODEL_PATH)
    metrics = {
        "model_version": model_version,
        "estimator": type(pipeline.named_steps["regressor"]).__name__,
        "rmse": rmse,
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
