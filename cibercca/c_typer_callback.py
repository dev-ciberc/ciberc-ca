from pathlib import Path

try:
    from .c_typer import app, typer
except Exception:
    from c_typer import app, typer  # noqa


class CallbackCommand(object):

    def path_inventory(self, value: Path):

        if value is None or value == "":
            raise typer.BadParameter("inventory is not directory",
                                     param_hint="--path")

        if value.is_dir():
            return value
        raise typer.BadParameter("inventory is not directory",
                                 param_hint="--path")

    def process_type(self, process: str):

        if process == "" or process is None:
            raise typer.BadParameter("process is not defined",
                                     param_hint="--process")

        if process not in ['src', 'dst']:
            raise typer.BadParameter("Only src or dst process",
                                     param_hint="--process")

        return process

    def output_type(self, output: str, name: str):

        if output not in ['json', 'excel']:
            raise typer.BadParameter("Only json or excel type is valid",
                                     param_hint="--output")

        if output == "excel" and name == "":
            raise typer.BadParameter(
                "a name has not been defined for the excel file",
                param_hint="--name")

        return output
