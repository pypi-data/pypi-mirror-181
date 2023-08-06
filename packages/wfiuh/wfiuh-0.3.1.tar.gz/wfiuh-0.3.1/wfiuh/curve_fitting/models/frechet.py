import dataclasses

import numpy as np
import numpy.typing as npt

from . import Model


@dataclasses.dataclass(kw_only=True)
class Frechet(Model):
    bounds: tuple[npt.ArrayLike, npt.ArrayLike] = dataclasses.field(
        default=([0, 0], np.inf)
    )

    @staticmethod
    def cdf(t: float | np.ndarray, a: float, b: float) -> float | np.ndarray:
        s = np.exp(-((t / b) ** -a))
        return s

    @staticmethod
    def pdf(t: float | np.ndarray, a: float, b: float) -> float | np.ndarray:
        u = a / b * (t / b) ** (-1 - a) * np.exp(-((t / b) ** (-a)))
        return u

    def prepare(
        self, x: np.ndarray, y: np.ndarray, func: str = "cdf"
    ) -> tuple[np.ndarray, np.ndarray]:
        return x[1:], y[1:]
