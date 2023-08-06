import dataclasses

import numpy as np

from . import Model


@dataclasses.dataclass(kw_only=True)
class Multistage(Model):
    @staticmethod
    def cdf(t: float | np.ndarray, a: float, b: float, c: float) -> float | np.ndarray:
        s = 1 - np.exp(-a * t - b * t**2 - c * t**3)
        return s

    @staticmethod
    def pdf(t: float | np.ndarray, a: float, b: float, c: float) -> float | np.ndarray:
        u = (a + 2 * b * t + 3 * c * t**2) * np.exp(-a * t - b * t**2 - c * t**3)
        return u
