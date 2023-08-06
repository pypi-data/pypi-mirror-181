import dataclasses

import numpy as np
import numpy.typing as npt
import scipy.special

from . import Model


@dataclasses.dataclass(kw_only=True)
class ShiftedLogPearson3(Model):
    bounds: tuple[npt.ArrayLike, npt.ArrayLike] = dataclasses.field(
        default=([0, 1, 0], np.inf)
    )

    @staticmethod
    def cdf(t: float | np.ndarray, a: float, b: float, c: float) -> float | np.ndarray:
        s = scipy.special.gammainc(b, c * np.log(t / a + 1))
        return s

    @staticmethod
    def pdf(t: float | np.ndarray, a: float, b: float, c: float) -> float | np.ndarray:
        u = (
            c**b
            * (np.log(t / a + 1)) ** (b - 1)
            / (a * scipy.special.gamma(b) * (t / a + 1) ** (c + 1))
        )
        return u
