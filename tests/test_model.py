from app.model import train


def test_train_reports_rmse_and_flag_metrics():
    metrics = train()
    assert metrics["rmse"] > 0
    assert metrics["high_risk_threshold"] > 0
    assert 0.0 <= metrics["precision"] <= 1.0
    assert 0.0 <= metrics["recall"] <= 1.0
