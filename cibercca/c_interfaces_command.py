from pathlib import Path
from typing import Optional

try:
    from .c_typer import app, typer
except Exception:
    from .c_typer import app, typer

try:
    from .c_interfaces import Interfaces
except Exception:
    from .c_interfaces import Interfaces


# almacena la informacion del estado para los comandos
state = {}


def callback_interface_output(value: str):  # noqa
    if value not in ['json', 'excel', 'database']:
        raise typer.BadParameter("Only json or excel type is valid",
                                 param_hint="--output")
    state['output'] = value
    return value


def callback_interface_path(value: Path):  # noqa
    if value.is_dir():
        return value
    raise typer.BadParameter("inventory is not directory",
                             param_hint="--path")


def callback_interface_mechanism(value: str):  # noqa
    if state['output'] == "excel":
        if value is None or value == "":
            raise typer.BadParameter(
                "no print mechanism defined",
                param_hint="--mechanism")
        if value not in ['row', 'column']:
            raise typer.BadParameter("Only row or column mechanisms",
                                     param_hint="--mechanism")
    return value


def callback_interface_name(value: str):  # noqa
    if state['output'] == "excel":
        if value is None or value == "":
            raise typer.BadParameter(
                "a name has not been defined for the excel file",
                param_hint="--name")
        return value


@app.command()
def interfaces(
    path: Optional[Path] = typer.Option(
        ...,
        help="The path to inventory",
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
    ),
    mechanism: Optional[str] = typer.Option(
        "",
        help="The excel mechanism to print report",
    ),
    name: Optional[str] = typer.Option(
        "",
        help="The name of excel report",
    ),
):
    """
    Device interface information

    Example:\n
        - python3 core/main.py interfaces --path=core/inventory/ --group=src --output=json > interfaces.json\n
        - python3 core/main.py interfaces --path=core/inventory/ --group=src --output=excel --mechanism=row --name=interfaces > interfaces.json
    """  # noqa

    # validaciones callback
    callback_interface_path(path)
    callback_interface_output(output)
    callback_interface_mechanism(mechanism)
    callback_interface_name(name)

    # se ejecuta si todas las validaciones
    # de los argumentos son correctas
    data = Interfaces(path=str(path), filter=group, workers=workers)
    data.run()

    # crea el proceso con estructura json
    if output == 'json':
        print(data.data_json())

    # para el reporte de excel se necesita
    # data, mechanism
    if output == 'excel':
        status = data.data_excel(mechanism, name)
        if status is False:
            return "excel not created."
        print(data.data_json())

    if output == 'database':
        print(data.data_database())
