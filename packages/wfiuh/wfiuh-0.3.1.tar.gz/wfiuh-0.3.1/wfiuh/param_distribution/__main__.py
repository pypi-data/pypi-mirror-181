import glob
import os
import typing

import click
import numpy as np
import pandas as pd
from rich.columns import Columns

from ..log import make_dict, make_series, print
from . import plot_params_distribution


@click.command(name="param-dis")
@click.option("--input-dir", type=click.Path(), default="results/params/cdf")
@click.option("--output-dir", type=click.Path(), default="results/param-dis/cdf/cdf")
@click.option("--key", default="cdf_r2_score")
@click.option(
    "--threshold-percentage", type=click.FloatRange(min=0, max=100), default=None
)
@click.option(
    "--threshold", show_default=True, type=click.FloatRange(min=0, max=1), default=0.9
)
def main(
    input_dir: str = "results/params/cdf",
    output_dir: str = "results/param-dis/cdf/cdf",
    key: str = "cdf_r2_score",
    threshold_percentage: typing.Optional[float] = None,
    threshold: float = 0.9,
):
    files = glob.glob(pathname=f"{input_dir}/*.csv")
    dfs: dict[str, pd.DataFrame] = dict()
    for filepath in files:
        name, _ = os.path.splitext(os.path.basename(filepath))
        df = pd.read_csv(filepath)
        df["model"] = name
        dfs[name] = df
    r2_score = pd.concat(
        [df[["id", "model", key]] for df in dfs.values()], ignore_index=True
    )
    columns = Columns()
    columns.add_renderable(
        make_series(r2_score[key].describe(), title="R2 Score Describe (All)")
    )
    if threshold_percentage:
        threshold = float(np.percentile(a=r2_score[key], q=threshold_percentage))
        columns.add_renderable(
            make_dict(
                {"percentage": threshold_percentage, key: threshold},
                title="R2 Score Threshold",
            )
        )
    else:
        columns.add_renderable(
            make_dict(
                {key: threshold},
                title="R2 Score Threshold",
            )
        )
    r2_score = r2_score[r2_score[key] > threshold]
    columns.add_renderable(
        make_series(r2_score[key].describe(), title="R2 Score Describe (Selected)")
    )
    columns.add_renderable(
        make_series(
            r2_score["model"].value_counts(), title="Catchment Counts (Selected)"
        )
    )
    print(columns)
    for name, df in dfs.items():
        df = df[df[key] > threshold]
        if df.empty:
            continue
        os.makedirs(name=output_dir, exist_ok=True)
        plot_params_distribution(data=df, fname=os.path.join(output_dir, f"{name}.png"))


if __name__ == "__main__":
    main()
