import os
from pathlib import Path
from typing import Optional

try:
    from .c_typer import app, typer
except Exception:
    from c_typer import app, typer  # noqa

try:
    from .c_records import Records
except Exception:
    from c_records import Records


@app.command()
def records(
    command: Optional[Path] = typer.Option(
        ...,
        help="The command for filter information en DB",
    )
):
    """
    Data for all device filter with command
    """

    if command:
        print(Records.findData(command))

    
    


