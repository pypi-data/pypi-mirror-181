import dataclasses

import numpy as np
import numpy.typing as npt

from . import Model


@dataclasses.dataclass(kw_only=True)
class DoublePower(Model):
    bounds: tuple[npt.ArrayLike, npt.ArrayLike] = dataclasses.field(
        default=([0, 1, 1], np.inf)
    )

    @staticmethod
    def cdf(t: float | np.ndarray, a: float, b: float, c: float) -> float | np.ndarray:
        s = (1 - (1 - t / a) ** b) ** c
        return s

    @staticmethod
    def pdf(t: float | np.ndarray, a: float, b: float, c: float) -> float | np.ndarray:
        u = (b * c / a) * (1 - t / a) ** (b - 1) * (1 - (1 - t / a) ** b) ** (c - 1)
        return u

    def prepare(
        self, x: np.ndarray, y: np.ndarray, func: str = "cdf"
    ) -> tuple[np.ndarray, np.ndarray]:
        self.p0 = [x.max() + 10, 2.0, 2.0]
        self.bounds = ([x.max(), 1.0, 1.0], np.inf)
        return x, y
