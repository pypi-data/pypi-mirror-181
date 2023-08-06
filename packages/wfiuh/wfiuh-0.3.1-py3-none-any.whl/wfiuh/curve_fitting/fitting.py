import itertools
from pathlib import Path

import numpy as np
import scipy.optimize
import sklearn.metrics

from .model import FUNCTIONS, Model
from .utils import prepare_y, read_csv


def curve_fitting(
    model: Model,
    x: np.ndarray,
    y: np.ndarray,
    fits: list[str] = ["cdf"],
    preds: list[str] = FUNCTIONS,
) -> dict:
    popts: dict = dict()
    for fit in fits:
        x, y = model.prepare(x, y, func=fit)
        popt, pcov = scipy.optimize.curve_fit(
            f=model.select(fit),
            xdata=x,
            ydata=prepare_y(x=x, y=y, func=fit),
            p0=model.p0,
            sigma=model.sigma,
            bounds=model.bounds,
        )
        popts[fit] = popt
    r2_scores: dict = dict()
    for fit, pred in itertools.product(fits, preds):
        try:
            r2_score = sklearn.metrics.r2_score(
                y_true=prepare_y(x=x, y=y, func=pred),
                y_pred=model.select(func=pred)(x, *popts[fit]),
            )
            r2_scores[fit, pred] = r2_score
        except:
            pass
    return {"popts": popts, "r2_scores": r2_scores}


def curve_fitting_file(
    model: Model,
    filepath: str | Path,
    fit: str = "cdf",
    preds: list[str] = FUNCTIONS,
) -> dict:
    id, x, y = read_csv(filepath=filepath)
    res = curve_fitting(model=model, x=x, y=y, fits=[fit], preds=preds)
    return {
        "id": id,
        "fit": fit,
        **{chr(ord("a") + i): p for i, p in enumerate(res["popts"][fit])},
        **{
            pred + "_r2_score": r2_score
            for (fit, pred), r2_score in res["r2_scores"].items()
        },
    }
