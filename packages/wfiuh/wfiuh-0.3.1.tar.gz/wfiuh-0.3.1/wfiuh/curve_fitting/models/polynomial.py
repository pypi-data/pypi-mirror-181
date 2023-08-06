import dataclasses

import numpy as np
import numpy.typing as npt

from . import Model


@dataclasses.dataclass(kw_only=True)
class Polynomial(Model):
    bounds: tuple[npt.ArrayLike, npt.ArrayLike] = dataclasses.field(
        default=(-np.inf, [0, np.inf, np.inf])
    )

    @staticmethod
    def cdf(t: float | np.ndarray, a: float, b: float, c: float) -> float | np.ndarray:
        return a * t**3 + b * t**2 + c * t

    @staticmethod
    def pdf(t: float | np.ndarray, a: float, b: float, c: float) -> float | np.ndarray:
        return 3 * a * t**2 + 2 * b * t + c
