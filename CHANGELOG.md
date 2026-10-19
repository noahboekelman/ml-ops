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


## v0.2 — Ridge + high-risk flag

### What changed from v0.1

- **Model:** swapped  `LinearRegression` for **`Ridge` (L2 regularization, `alpha=10`)**, that was kept inside the same `StandardScaler` pipeline.
- **High-risk flag:** we now turn the continuous progression score into a triage decision, that is, a patient is flagged "high risk" when their predicted progression lands at or above the **75th percentile of the training targets** (threshold = 214). The flag is measured with precision and recall on the held-out split.

### Metrics (v0.1 vs v0.2, same seeded split)

| Version | Model                             | Held-out RMSE       | High-risk precision | High-risk recall |
|---------|-----------------------------------|---------------------|---------------------|------------------|
| v0.1    | StandardScaler + LinearRegression | 58.52               | 0.50                | 0.30 |
| v0.2    | StandardScaler + Ridge (α=10)     | 58.56               | 0.55                | 0.30 |

### Why this is an improvement

The dataset is small, 442 patients, and close to linear, so no model really beats the baseline on RMSE, atleast in any meaningful sense. We did try, and the error stayed flat 58.52 → 58.56 within noise. So rather than focusing on the RMSE metric, v0.2 improves the thing the clinic does actually cares about which is how well the model picks who to follow up with.

- **Fewer false alarms.** At the same recall (0.30), the high-risk flag's precision rises from 0.50 to 0.55, which means of the patients we flag for a follow-up call, a larger share are actual high risk. That's less wasted nurse time.
- **More robust by design.** Ridge's regularization stops the model from over-reacting to noise and correlated features, which is the sensible choice for a small clinical dataset It also holds RMSE steady while doing so.
- **A real triage capability.** v0.1 only produced a score while v0.2 adds a measurable high-risk decision (precision and recall), which maps directly to the goal of prioritising follow-ups that are neccesary.

In short, v0.2 keeps the accuracy of v0.1 but makes the triage decision cleaner and the model more robust.

### What we also tried

We looked at whether we could make the flag catch more of the actual high-risk patients. Instead of a fixed cut-off, we used cross-validation to let the data choose the cut-off for us. It looked promising on the patients the model had already learned from, but on new patients it didn't actually help as recall only moved to about 0.35 while precision dropped to about 0.37, so the overall score F1 ≈ 0.36 was no better than the simple cut-off of F1 ≈ 0.39. It caught a few more high-risk cases but raised more false alarms, so we kept the simple, fixed cut-off.