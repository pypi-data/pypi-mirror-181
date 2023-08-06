from .. import Model
from .beta import Beta
from .double_power import DoublePower
from .double_triangular import DoubleTriangular
from .frechet import Frechet
from .gamma import Gamma
from .hill import Hill
from .hoerl import Hoerl
from .inverse_gaussian import InverseGaussian
from .kumaraswamy import Kumaraswamy
from .logistic import Logistic
from .multistage import Multistage
from .normal_gaussian import NormalGaussian
from .polynomial import Polynomial
from .rational import Rational
from .shiftred_log_pearson_3 import ShiftedLogPearson3
from .weibull import Weibull

NAME_TO_MODEL = {
    "Beta": Beta,
    "DoublePower": DoublePower,
    "DoubleTriangular": DoubleTriangular,
    "Frechet": Frechet,
    "Gamma": Gamma,
    "Hill": Hill,
    "Hoerl": Hoerl,
    "InverseGaussian": InverseGaussian,
    "Kumaraswamy": Kumaraswamy,
    "Logistic": Logistic,
    "Multistage": Multistage,
    "NormalGaussian": NormalGaussian,
    "Polynomial": Polynomial,
    "Rational": Rational,
    "ShiftedLogPearson3": ShiftedLogPearson3,
    "Weibull": Weibull,
}
