from __future__ import annotations

from sklearn.ensemble import RandomForestRegressor


class WindModel:
    def __init__(self):
        self.model = RandomForestRegressor(n_estimators=20, random_state=42)

    def fit(self, X, y):
        self.model.fit(X, y)
        return self

    def predict(self, X):
        return self.model.predict(X)
