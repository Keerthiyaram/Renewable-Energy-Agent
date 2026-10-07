from __future__ import annotations

import pandas as pd


def train_model(model, X: pd.DataFrame, y: pd.Series):
    model.fit(X, y)
    return model
