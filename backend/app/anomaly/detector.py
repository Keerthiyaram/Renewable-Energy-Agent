from __future__ import annotations

import numpy as np


class ZScoreDetector:
    def detect(self, values: list[float], threshold: float = 2.0):
        values_array = np.asarray(values, dtype=float)
        if values_array.size < 2:
            return []
        mean = values_array.mean()
        std = values_array.std(ddof=0)
        if std == 0:
            return []
        scores = np.abs((values_array - mean) / std)
        return [float(score) for score in scores if score > threshold]
