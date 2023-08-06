import dataclasses

import numpy as np
import numpy.typing as npt
import scipy.stats

from . import Model


@dataclasses.dataclass(init=True, kw_only=True)
class NormalGaussian(Model):
    bounds: tuple[npt.ArrayLike, npt.ArrayLike] = dataclasses.field(
        default=([-np.inf, 0], np.inf)
    )

    @staticmethod
    def cdf(t: float | np.ndarray, a: float, b: float) -> float | np.ndarray:
        return scipy.stats.norm.cdf(x=t, loc=a, scale=b)

    @staticmethod
    def pdf(t: float | np.ndarray, a: float, b: float) -> float | np.ndarray:
        return scipy.stats.norm.pdf(x=t, loc=a, scale=b)
