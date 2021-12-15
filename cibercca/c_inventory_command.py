import os

try:
    from .c_typer import app, typer
except Exception:
    from c_typer import app, typer

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


@app.command()
def inventory(
    create: bool = typer.Option(
        "",
        help="create files from inventory examples",
    ),
):
    """
    Create files for inventory system
    """
    if create:
        exists = os.path.exists("./inventory/")
        if not exists:
            os.system(f"cp -r {BASE_DIR}/inventory/ .")
        else:
            print("inventory already exists")
