import dataclasses

import numpy as np
import numpy.typing as npt

from . import Model

SCALE = 150


@dataclasses.dataclass(kw_only=True)
class Kumaraswamy(Model):
    bounds: tuple[npt.ArrayLike, npt.ArrayLike] = dataclasses.field(
        default=([0, 0], np.inf)
    )

    @staticmethod
    def cdf(t: float | np.ndarray, a: float, b: float) -> float | np.ndarray:
        t /= SCALE
        s = 1 - (1 - t**a) ** b
        return s

    @staticmethod
    def pdf(t: float | np.ndarray, a: float, b: float) -> float | np.ndarray:
        t /= SCALE
        u = a * b * t ** (a - 1) * (1 - t**a) ** (b - 1)
        return u
