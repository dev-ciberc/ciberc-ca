import os
import platform

try:
    from .c_typer import app, typer
except Exception:
    from .c_typer import app, typer

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
    system = platform.system()

    if create:
        exists = os.path.exists("./inventory/")
        if not exists:
            if system == "Windows":
                os.system(f"xcopy /E /I \"{BASE_DIR}\\inventory\" .\\inventory")
            elif system in ["Linux", "Darwin"]:
                os.system(f"cp -r {BASE_DIR}/inventory/ .")
            else:
                print(f"Unsupported OS: {system}")
        else:
            print("Inventory already exists")
