import dataclasses

import numpy as np
import numpy.typing as npt
import scipy.stats

from . import Model


@dataclasses.dataclass(kw_only=True)
class Gamma(Model):
    bounds: tuple[npt.ArrayLike, npt.ArrayLike] = dataclasses.field(
        default=([0, 1], np.inf)
    )

    @staticmethod
    def cdf(t: float | np.ndarray, a: float, b: float) -> float | np.ndarray:
        return scipy.stats.gamma.cdf(t, b, loc=0, scale=a)

    @staticmethod
    def pdf(t: float | np.ndarray, a: float, b: float) -> float | np.ndarray:
        return scipy.stats.gamma.pdf(t, b, loc=0, scale=a)
