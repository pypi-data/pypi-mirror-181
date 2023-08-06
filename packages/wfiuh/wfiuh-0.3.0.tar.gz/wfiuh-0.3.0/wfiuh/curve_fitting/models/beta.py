import dataclasses

import numpy as np
import numpy.typing as npt
import scipy.stats

from . import Model

SCALE = 150


@dataclasses.dataclass(kw_only=True)
class Beta(Model):
    bounds: tuple[npt.ArrayLike, npt.ArrayLike] = dataclasses.field(
        default=([1, 0], np.inf)
    )

    @staticmethod
    def cdf(t: float | np.ndarray, a: float, b: float) -> float | np.ndarray:
        s = scipy.stats.beta.cdf(t, a, b, scale=SCALE)
        return s

    @staticmethod
    def pdf(t: float | np.ndarray, a: float, b: float) -> float | np.ndarray:
        u = scipy.stats.beta.pdf(t, a, b, scale=SCALE)
        return u
