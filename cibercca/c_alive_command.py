import os
from typing import Optional

try:
    from .c_typer import app, typer
except Exception:
    from c_typer import app, typer  # noqa

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

try:
    from .c_alive import Alive
except Exception:
    from c_alive import Alive


@app.command()
def alive(
    path: Optional[str] = None,
    group: Optional[str] = None,
    workers: Optional[int] = None,
    output: Optional[str] = None,
):
    """
    alive for all device filter with groups
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
