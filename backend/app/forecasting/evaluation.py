from __future__ import annotations

from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def evaluate_model(model, X, y):
    predictions = model.predict(X)
    return {
        "mae": float(mean_absolute_error(y, predictions)),
        "rmse": float(mean_squared_error(y, predictions, squared=False)),
        "r2": float(r2_score(y, predictions)),
    }
