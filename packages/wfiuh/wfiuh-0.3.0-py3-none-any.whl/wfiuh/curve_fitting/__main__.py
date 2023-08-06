import concurrent.futures
import glob
import os
import signal
import sys
from pathlib import Path

import click
import pandas as pd
from rich.columns import Columns
from rich.console import Console, Group
from rich.live import Live
from rich.panel import Panel
from rich.pretty import Pretty
from rich.progress import (
    BarColumn,
    MofNCompleteColumn,
    Progress,
    TaskProgressColumn,
    TextColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
)

from ..log import make_series
from .fitting import curve_fitting_file
from .model import FUNCTIONS, Model
from .models import NAME_TO_MODEL


def initializer():
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    sys.stderr = open(file=os.devnull, mode="w")


def save_results(
    results: list[dict],
    filepath: str,
    model_name: str,
    fit: str = "cdf",
    preds: list[str] = FUNCTIONS,
    console: Console = Console(),
) -> None:
    if not results:
        return
    df = pd.DataFrame.from_records(data=results, index="id")
    df.sort_index(inplace=True)
    columns = Columns()
    for pred in preds:
        panel = make_series(
            series=df[pred + "_r2_score"].describe(),
            title=f"{model_name} {fit} -> {pred} R2 Score",
        )
        columns.add_renderable(panel)
    console.print(columns)
    os.makedirs(name=os.path.dirname(filepath), exist_ok=True)
    df.to_csv(filepath)


def main(
    input_dir: str | Path = "2-sub-WFIUH_rescaled",
    output_dir: str | Path = "results/params/cdf",
    models: list[Model] = list(NAME_TO_MODEL.values()),
    fit: str = "cdf",
    preds: list[str] = FUNCTIONS,
    verbose: bool = False,
) -> int:
    files = glob.glob(pathname=f"{input_dir}/*.csv")
    overall_progress = Progress(
        TextColumn(text_format="{task.description}", style="logging.level.info"),
        BarColumn(),
        TaskProgressColumn(),
        MofNCompleteColumn(),
        TimeElapsedColumn(),
    )
    models_progress = Progress(
        TextColumn(text_format="{task.description}", style="logging.level.info"),
        BarColumn(),
        TaskProgressColumn(),
        MofNCompleteColumn(),
        TimeElapsedColumn(),
        TimeRemainingColumn(),
    )
    progress_group = Group(
        Panel(models_progress, expand=False),
        Panel(overall_progress, expand=False),
    )
    with Live(progress_group) as live:
        overview_task_id = overall_progress.add_task(description="Overall Progress")
        for model in overall_progress.track(models, task_id=overview_task_id):
            model_task_id = models_progress.add_task(
                description=f"{model.name} {fit}", total=len(files)
            )
            results: list[dict] = []
            try:
                with concurrent.futures.ProcessPoolExecutor(
                    initializer=initializer
                ) as pool:
                    futures: list[concurrent.futures.Future] = list(
                        map(
                            lambda filepath: pool.submit(
                                curve_fitting_file,
                                model=model,
                                filepath=filepath,
                                fit=fit,
                                preds=preds.copy(),
                            ),
                            files,
                        )
                    )
                    for future in concurrent.futures.as_completed(futures):
                        try:
                            result = future.result()
                            if result:
                                results.append(result)
                                models_progress.advance(task_id=model_task_id)
                        except KeyboardInterrupt as e:
                            raise e
                        except Exception as e:
                            if verbose:
                                live.console.log(
                                    model.name,
                                    fit,
                                    Pretty(e),
                                    style="logging.level.error",
                                )
            except KeyboardInterrupt as e:
                save_results(
                    results,
                    os.path.join(output_dir, f"{model.name}.csv"),
                    model_name=model.name,
                    fit=fit,
                    preds=preds,
                    console=live.console,
                )
                raise e
            except Exception as e:
                live.console.print_exception()
            else:
                save_results(
                    results,
                    os.path.join(output_dir, f"{model.name}.csv"),
                    model_name=model.name,
                    fit=fit,
                    preds=preds,
                    console=live.console,
                )
            finally:
                models_progress.stop_task(model_task_id)
    return 0


@click.command(name="curve-fitting")
@click.option("--input-dir", type=click.Path(), default="2-sub-WFIUH_rescaled")
@click.option("--output-dir", type=click.Path(), default="results/params/cdf")
@click.option(
    "--model",
    type=click.Choice(choices=list(NAME_TO_MODEL.keys())),
    default=list(NAME_TO_MODEL.keys()),
    multiple=True,
)
@click.option("--fit", type=click.Choice(choices=FUNCTIONS), default="cdf")
@click.option(
    "--pred", type=click.Choice(choices=FUNCTIONS), default=FUNCTIONS, multiple=True
)
@click.option("--verbose", is_flag=True)
def command(
    input_dir: str | Path = "2-sub-WFIUH_rescaled",
    output_dir: str | Path = "results/params/cdf",
    model: tuple[str] = tuple(NAME_TO_MODEL.keys()),
    fit: str = "cdf",
    pred: tuple[str] = tuple(FUNCTIONS),
    verbose: bool = False,
) -> None:
    main(
        input_dir=input_dir,
        output_dir=output_dir,
        models=[NAME_TO_MODEL[name]() for name in model],
        fit=fit,
        preds=list(pred),
        verbose=verbose,
    )


if __name__ == "__main__":
    command()
