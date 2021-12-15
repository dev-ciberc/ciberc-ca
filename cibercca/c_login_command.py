from typing import Optional

try:
    from .c_typer import app, typer
except Exception:
    from c_typer import app, typer

try:
    from .c_login import Login
except Exception:
    from c_login import Login


def callback_validate_name(value: str):
    if value is None or value == "":
        raise typer.BadParameter(
            "a name has not been defined",
            param_hint="--name")
    return value


def callback_validate_password(value: str):
    if value is None or value == "":
        raise typer.BadParameter(
            "password is required",
            param_hint="--password")
    return value


@app.command()
def login(
    name: Optional[str] = typer.Option(
        ...,
        help="The name user for ciberc-ca",
        callback=callback_validate_name
    ),
    password: str = typer.Option(
        ...,
        prompt=True,
        confirmation_prompt=True,
        hide_input=True,
        callback=callback_validate_password)
):
    """
    Login on (CiberC Code Automations)
    """

    try:
        login = Login()
        login.init(username=name, password=password)
        login.saveToken()

        if login.getToken() is None:
            raise typer.BadParameter(
                "error to login on ciberc-ca")
    except Exception:
        raise typer.BadParameter(
            "error to login on ciberc-ca")

    message = typer.style("login success", fg=typer.colors.GREEN, bold=True)
    typer.echo(message)
