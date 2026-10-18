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

### Service

- `GET /health` → `{"status": "ok", "model_version": "v0.1"}`.
- `POST /predict` → `{"prediction": <float>}`.
- Invalid input (missing/invalid feature) → HTTP `422` with a JSON validation error.
- Model is trained during the Docker build and baked into the image.
