import click

from .best_sample.__main__ import command as best_sample
from .curve_fitting.__main__ import command as curve_fitting
from .param_distribution.__main__ import main as param_distribution


@click.group(name="wfiuh", context_settings={"show_default": True})
def main() -> None:
    pass


main.add_command(cmd=best_sample)
main.add_command(cmd=curve_fitting)
main.add_command(cmd=param_distribution)


if __name__ == "__main__":
    main()
