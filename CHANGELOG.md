# Changelog

All notable changes to the diabetes progression triage service are documented here.

## v0.1 — Baseline

Initial release of the ML triage service.

### Model

- **Pipeline:** `StandardScaler` + `LinearRegression`.
- **Dataset:** scikit-learn Diabetes regression dataset (`load_diabetes`), target treated as a progression index (higher = greater deterioration risk).
- **Validation:** single held-out split, `test_size=0.2`, `random_state=0`.

### Metrics

| Version | Model | Held-out RMSE |
|---------|-------|---------------|
| v0.1    | StandardScaler + LinearRegression | **58.52** |

Metrics are regenerated deterministically on every train and written to `app/model_store/metrics.json`.

### Reasoning

- **Start simple.** The dataset is small, 442 patients, and the signal is close to linear, so a plain linear regression seemed as a reasonable fit. We also tried a Random Forest and it scored worse here, which confirmed that starting simple was the right call.
- **Scaler and model in one pipeline.** Bundling the preprocessing with the model means the exact same scaling is applied when training and when predicting, and so the two can never drift apart.
- **Fixed seed and split.** The random seed and train/test split are pinned, so anyone who runs training again wiil get the same model and the same RMSE. So it's deterministic and reproducible by default.
- **RMSE as the metric.** It is in the same units as the progression score, so the error reads directly --> predictions are off by ~58 progression points on average.
- **Training and serving kept separate.** Training writes the model to `app/model_store/`, and the API loads it lazily on the first request, so the app can start and answer `/health` without needing a model file.

### Service

- `GET /health` → `{"status": "ok", "model_version": "v0.1"}`.
- `POST /predict` → `{"prediction": <float>}`.
- Invalid input (missing/invalid feature) → HTTP `422` with a JSON validation error.
- The API loads the trained model from `app/model_store/` at runtime, lazily on the first request.
