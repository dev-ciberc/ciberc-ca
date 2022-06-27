import os
from pathlib import Path
from typing import Optional

try:
    from .c_typer import app, typer
except Exception:
    from c_typer import app, typer  # noqa

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

try:
    from .c_ping_src import SourceNetwork
except Exception:
    from c_ping_src import SourceNetwork


try:
    from .c_ping_dst import DestinationNetwork
except Exception:
    from c_ping_dst import DestinationNetwork  # noqa


try:
    from .c_typer_callback import CallbackCommand
except Exception:
    from c_typer_callback import CallbackCommand  # noqa


# estado de los comandos
state = {}


def callback_path(value: Path):  # noqa
    if value.is_dir():
        return value
    raise typer.BadParameter("inventory is not directory",
                             param_hint="--path")


def callback_output(value: str):
    if value not in ['json', 'excel']:
        raise typer.BadParameter("Only json or excel type is valid",
                                 param_hint="--output")

    state['output'] = value
    return value


def callback_name(value: str):
    if state['output'] == "excel":
        if value is None or value == "":
            raise typer.BadParameter(
                "a name has not been defined for the excel file",
                param_hint="--name")
    return value


def callback_process(process: str):
    if process not in ['src', 'dst']:
        raise typer.BadParameter("Only src or dst process",
                                 param_hint="--process")
    state['process'] = process
    return process


def callback_input(input: str):
    if state["process"] == "dst":
        if input is None or input == "":
            raise typer.BadParameter("no input file defined",
                                     param_hint="--input")

        extension = os.path.splitext(input)[1]
        if extension not in ['.json', '.excel']:
            raise typer.BadParameter("Only json or excel input for process dst",  # noqa
                                     param_hint="--input")
    return input


@app.command()
def ping(
    path: Optional[Path] = typer.Option(
        ...,
        help="The path to inventory",
        callback=callback_path
    ),
    group: Optional[str] = typer.Option(
        ...,
        help="The groups to filter inventory"
    ),
    workers: Optional[int] = typer.Option(
        2,
        help="The parallel execution"
    ),
    output: Optional[str] = typer.Option(
        "json",
        help="The type to print report",
        callback=callback_output
    ),
    name: Optional[str] = typer.Option(
        "",
        help="The name of the excel file",
        callback=callback_name
    ),
    process: Optional[str] = typer.Option(
        ...,
        help="what type of process for the vrf report [src, dst]",
        callback=callback_process
    ),
):
    """
    report por vrf and ping results for inventory devices
    """

    # --
    # define the process type for the report
    # --
    if process == "src":
        data = SourceNetwork(path=path, filter=group, workers=workers)
        data.run()

    if process == "dst":
        data = DestinationNetwork(path=path, filter=group, workers=workers)
        data.run()

    # --
    # define the output type for the report
    # --
    if output == "json":
        print(data.data_json())

    if output == "excel":
        status = data.data_excel(name=name)
        if status is False:
            return "excel not created."
        print(data.data_json())
