import dataclasses

import numpy as np

from . import Model


@dataclasses.dataclass(kw_only=True)
class Rational(Model):
    @staticmethod
    def cdf(t: float | np.ndarray, a: float, b: float, c: float) -> float | np.ndarray:
        return a * t / (1 + b * t + c * t**2)

    @staticmethod
    def pdf(t: float | np.ndarray, a: float, b: float, c: float) -> float | np.ndarray:
        return a * (1 - c * t**2) / (1 + b * t + c * t**2) ** 2
