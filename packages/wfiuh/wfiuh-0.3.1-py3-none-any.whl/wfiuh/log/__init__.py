import typing

import pandas as pd
from rich import print
from rich.console import RenderableType
from rich.padding import PaddingDimensions
from rich.panel import Panel
from rich.pretty import Pretty
from rich.pretty import install as pretty_install
from rich.style import Style
from rich.table import Table
from rich.text import Text
from rich.traceback import install as traceback_install

pretty_install()
traceback_install()
panel_title_style = Style(color="bright_blue", bold=True)


def make_panel(
    obj: RenderableType,
    *args,
    title: typing.Optional[str] = None,
    expand: bool = False,
    **kwargs,
) -> Panel:
    panel = Panel(
        obj,
        *args,
        title=Text(text=title, style=panel_title_style) if title else None,
        expand=expand,
        **kwargs,
    )
    return panel


def print_panel(
    obj: RenderableType,
    *args,
    title: typing.Optional[str] = None,
    expand: bool = False,
    **kwargs,
) -> None:
    panel = make_panel(obj=obj, *args, title=title, expand=expand, **kwargs)
    print(panel)


def make_data_frame(
    data_frame: pd.DataFrame,
    *args,
    title: typing.Optional[str] = None,
    expand: bool = False,
    padding: PaddingDimensions = (0, 4),
    **kwargs,
) -> Panel:
    table = Table.grid(padding=padding)
    for key, values in data_frame.items():
        table.add_row(str(key), *map(Pretty, values))
    panel = make_panel(table, *args, title=title, expand=expand, **kwargs)
    return panel


def print_data_frame(
    data_frame: pd.DataFrame,
    *args,
    title: typing.Optional[str] = None,
    expand: bool = False,
    padding: PaddingDimensions = (0, 4),
    **kwargs,
) -> None:
    panel = make_data_frame(
        data_frame=data_frame,
        *args,
        title=title,
        expand=expand,
        padding=padding,
        **kwargs,
    )
    print(panel)


def make_series(
    series: pd.Series,
    *args,
    title: typing.Optional[str] = None,
    expand: bool = False,
    padding: PaddingDimensions = (0, 4),
    **kwargs,
) -> Panel:
    table = Table.grid(padding=padding)
    for key, value in series.items():
        table.add_row(str(key), Pretty(value))
    panel = make_panel(table, *args, title=title, expand=expand, **kwargs)
    return panel


def print_series(
    series: pd.Series,
    *args,
    title: typing.Optional[str] = None,
    expand: bool = False,
    padding: PaddingDimensions = (0, 4),
    **kwargs,
) -> None:
    panel = make_series(
        series=series, *args, title=title, expand=expand, padding=padding, **kwargs
    )
    print(panel)


def make_dict(
    obj: dict,
    *args,
    title: typing.Optional[str] = None,
    expand: bool = False,
    padding: PaddingDimensions = (0, 4),
    **kwargs,
) -> Panel:
    series = pd.Series(obj)
    panel = make_series(
        series=series, *args, title=title, expand=expand, padding=padding, **kwargs
    )
    return panel


def print_dict(
    obj: dict,
    *args,
    title: typing.Optional[str] = None,
    expand: bool = False,
    padding: PaddingDimensions = (0, 4),
    **kwargs,
) -> None:
    panel = make_dict(
        obj=obj, *args, title=title, expand=expand, padding=padding, **kwargs
    )
    print(panel)
