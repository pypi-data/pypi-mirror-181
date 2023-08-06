import dataclasses

import numpy as np

from . import Model


@dataclasses.dataclass(kw_only=True)
class Logistic(Model):
    @staticmethod
    def cdf(t: float | np.ndarray, a: float, b: float, c: float) -> float | np.ndarray:
        s = a / (1 + b * np.exp(-c * t))
        return s

    @staticmethod
    def pdf(t: float | np.ndarray, a: float, b: float, c: float) -> float | np.ndarray:
        u = a * b * c * np.exp(-c * t) / (b + np.exp(c * t) ** 2)
        return u
