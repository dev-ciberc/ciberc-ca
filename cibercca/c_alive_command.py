import sys
import os
from pathlib import Path
from typing import Optional
from .c_alive import Alive

try:
    from .c_typer import app, typer
except Exception:
    from .c_typer import app, typer  # noqa

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@app.command()
def alive(
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
):
    """
    Alive for all device filter with groups
    """

    if path is None:
        path_inventory = BASE_DIR + "/inventory/"
    else:
        path_inventory = path

    alive = Alive(path=path_inventory, filter=group, workers=workers)
    alive.run()

    if output == 'json':
        print(alive.data_json())

    if output == 'table':
        print(alive.data_table())
    
    if output == 'database':
        print(alive.data_database())
    
