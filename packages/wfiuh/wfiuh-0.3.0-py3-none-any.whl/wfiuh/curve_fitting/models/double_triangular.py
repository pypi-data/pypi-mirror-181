import dataclasses

import numpy as np
import numpy.typing as npt

from . import Model


@dataclasses.dataclass(kw_only=True)
class DoubleTriangular(Model):
    bounds: tuple[npt.ArrayLike, npt.ArrayLike] = dataclasses.field(
        default=([0, 0], [np.inf, 1])
    )

    @staticmethod
    def cdf(t: float | np.ndarray, a: float, b: float) -> float | np.ndarray:
        def kernel(t: float) -> float:
            if 0 <= t and t <= b * a:
                return (t / a) ** 2 / b
            elif b * a <= t and t <= a:
                return 1 - (1 - t / a) ** 2 / (1 - b)
            else:
                return 0  # nan

        if isinstance(t, np.ndarray):
            return np.array(list(map(kernel, t)))
        else:
            return kernel(t)

    @staticmethod
    def pdf(t: float | np.ndarray, a: float, b: float) -> float | np.ndarray:
        def kernel(t: float) -> float:
            if 0 <= t and t <= b * a:
                return 2 * t / a / (a * b)
            elif b * a <= t and t <= a:
                return 2 * (1 - t / a) / (a * (1 - b))
            else:
                return 0  # nan

        if isinstance(t, np.ndarray):
            return np.array(list(map(kernel, t)))
        else:
            return kernel(t)

    def prepare(
        self, x: np.ndarray, y: np.ndarray, func: str = "cdf"
    ) -> tuple[np.ndarray, np.ndarray]:
        self.p0 = [x.max() + 10, 0.5]
        self.bounds = ([x.max(), 0], [np.inf, 1])
        return x, y
