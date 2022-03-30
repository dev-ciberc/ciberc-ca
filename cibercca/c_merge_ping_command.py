from typing import Optional
import os

try:
    from .c_typer import app, typer
except Exception:
    from c_typer import app, typer  # noqa

try:
    from .c_merge_ping import PingMerge
except Exception:
    from c_merge_ping import PingMerge  # noqa


# --
# mantiene el estado de los comandos
state = {}


def callback_file_extension(value: str):
    ext = os.path.splitext(value)[1]

    if ext in [".xlsx", ".xls", ".json", ".csv"]:
        return value
    else:
        raise typer.BadParameter(
            "The file format must be .xlsx, .xls, .json o .csv"
        )


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


@app.command()
def ping_merge(
    file_src: Optional[str] = typer.Option(
        ...,
        help="Vrf origin listing file",
        callback=callback_file_extension
    ),
    file_dst: Optional[str] = typer.Option(
        ...,
        help="Target vrf listing file",
        callback=callback_file_extension
    ),
    output: Optional[str] = typer.Option(
        ...,
        help="The type to print report",
        callback=callback_output
    ),
    name: Optional[str] = typer.Option(
        "",
        help="The name of the excel file",
        callback=callback_name
    ),

):
    """
    Command to merge the source vrf listing files and
    destination with validated report
    """
    ping = PingMerge(file_src, file_dst)
    ping.run()

    # --
    # define the output type for the report
    # --
    if output == "json":
        print(ping.data_json())

    if output == "excel":
        status = ping.data_excel(file_name=name)
        if status is False:
            return "excel not created."
        print(ping.data_json())
