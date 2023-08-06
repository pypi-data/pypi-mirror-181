import dataclasses

import numpy as np
import numpy.typing as npt
import scipy.stats

from . import Model


@dataclasses.dataclass(kw_only=True)
class InverseGaussian(Model):
    bounds: tuple[npt.ArrayLike, npt.ArrayLike] = dataclasses.field(
        default=([0, 0], np.inf)
    )

    @staticmethod
    def cdf(t: float | np.ndarray, a: float, b: float) -> float | np.ndarray:
        return scipy.stats.invgauss.cdf(x=t, mu=b / a, scale=a)

    @staticmethod
    def pdf(t: float | np.ndarray, a: float, b: float) -> float | np.ndarray:
        return scipy.stats.invgauss.pdf(x=t, mu=b / a, scale=a)
