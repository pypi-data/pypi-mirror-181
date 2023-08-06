from pathlib import Path

import click
import pandas as pd

from ..curve_fitting import NAME_TO_MODEL, Model
from ..curve_fitting.utils import read_csv
from ..log import print
from . import plot_fitting


def main(
    model: Model,
    param_path: str | Path,
    output: str | Path,
    key: str = "pdf_r2_score",
    threshold: float = 0.9,
    data_path: str | Path = "2-sub-WFIUH_rescaled",
):
    df = pd.read_csv(param_path)
    idx_max = df[key].idxmax()
    if df[key][idx_max] < threshold:
        print(f"{key} = {df[key][idx_max]} < {threshold}")
        return
    id = df["id"][idx_max]
    data_path = Path(data_path) / f"{id}_wfiuh.csv"
    id_, x, y = read_csv(data_path)
    assert id == id_
    plot_fitting(model=model, x=x, y=y, output=output, id=id)


@click.command("best-sample")
@click.option(
    "-m",
    "--model",
    type=click.Choice(choices=list(NAME_TO_MODEL.keys())),
    required=True,
)
@click.option(
    "--param-path",
    type=click.Path(exists=True, file_okay=True, dir_okay=False),
    required=True,
)
@click.option("-o", "--output", type=click.Path(), required=True)
@click.option("--key", default="pdf_r2_score")
@click.option("--threshold", type=click.FloatRange(max=1), default=0.9)
@click.option(
    "--data-path",
    type=click.Path(exists=True, file_okay=False, dir_okay=True),
    default="2-sub-WFIUH_rescaled",
)
def command(
    model: str,
    param_path: str | Path,
    output: str | Path,
    key: str = "pdf_r2_score",
    threshold: float = 0.9,
    data_path: str | Path = "2-sub-WFIUH_rescaled",
):
    main(
        model=NAME_TO_MODEL[model](),
        param_path=param_path,
        output=output,
        key=key,
        threshold=threshold,
        data_path=data_path,
    )


if __name__ == "__main__":
    command()
