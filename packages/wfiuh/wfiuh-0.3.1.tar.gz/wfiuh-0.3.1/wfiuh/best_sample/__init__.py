import itertools
import os
import typing
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from rich.pretty import Pretty
from rich.table import Table

from ..curve_fitting import Model, curve_fitting
from ..curve_fitting.utils import prepare_y
from ..log import print


def prepare_plot(
    model: Model, x: np.ndarray, y: np.ndarray, fit: str = "cdf", pred: str = "cdf"
) -> tuple[float, pd.DataFrame]:
    res = curve_fitting(model=model, x=x, y=y, fits=[fit], preds=[pred])
    r2_score = typing.cast(dict, res["r2_scores"]).get((fit, pred), np.nan)
    popt = res["popts"][fit]
    pred_x = np.linspace(start=x.min(), stop=x.max(), num=1000)
    pred_y = model.select(pred)(pred_x, *popt)
    return r2_score, pd.concat(
        [
            pd.DataFrame(
                {
                    "x": x,
                    "y": prepare_y(x=x, y=y, func=pred),
                    "hue": "true",
                    "fit": fit,
                    "predict": pred,
                }
            ),
            pd.DataFrame(
                {
                    "x": pred_x,
                    "y": pred_y,
                    "hue": "predict",
                    "fit": fit,
                    "predict": pred,
                }
            ),
        ]
    )


def annotate_r2_score(
    data: pd.DataFrame, label: str, r2_scores: dict, *args, **kwargs
) -> None:
    if label == "true":
        return
    fit = data["fit"][0]
    pred = data["predict"][0]
    plt.text(
        x=data["x"].max(),
        y=(data["y"].min() + data["y"].max()) / 2,
        s=r"$R^2 = {:.5f}$".format(r2_scores[fit, pred]),
        horizontalalignment="right",
        usetex=True,
        verticalalignment="center",
    )


def plot_fitting(
    model: Model,
    x: np.ndarray,
    y: np.ndarray,
    output: str | Path,
    id: typing.Optional[int] = None,
) -> None:
    dfs: list[pd.DataFrame] = list()
    r2_scores: dict = dict()
    table = Table("fit", "predict", "r2_score", title=model.name)
    for fit, pred in itertools.product(["cdf", "pdf"], repeat=2):
        r2_score, df = prepare_plot(model=model, x=x, y=y, fit=fit, pred=pred)
        r2_scores[fit, pred] = r2_score
        table.add_row(fit, pred, Pretty(r2_score))
        dfs.append(df)
    print(table)
    data = pd.concat(dfs)
    plt.figure(dpi=300)
    g = sns.FacetGrid(
        data=data,
        row="predict",
        col="fit",
        hue="hue",
        sharex="col",
        sharey="row",
        legend_out=False,
    )
    g.map_dataframe(sns.lineplot, "x", "y")
    g.map_dataframe(annotate_r2_score, r2_scores=r2_scores)
    if id:
        g.add_legend(title=f"id = {id}")
    else:
        g.add_legend()
    g.tight_layout()
    os.makedirs(name=Path(output).parent, exist_ok=True)
    plt.savefig(output)
    plt.close()
