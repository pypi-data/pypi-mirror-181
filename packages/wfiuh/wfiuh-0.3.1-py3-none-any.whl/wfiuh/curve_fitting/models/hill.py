import dataclasses

import numpy as np

from . import Model


@dataclasses.dataclass(kw_only=True)
class Hill(Model):
    @staticmethod
    def cdf(t: float | np.ndarray, a: float, b: float, c: float) -> float | np.ndarray:
        s = a * t**b / (c**b + t**b)
        return s

    @staticmethod
    def pdf(t: float | np.ndarray, a: float, b: float, c: float) -> float | np.ndarray:
        u = a * b * c**b * t ** (b - 1) / (c**b + t**b) ** 2
        return u
