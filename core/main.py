try:
    from .c_typer import app
except Exception:
    from c_typer import app


# tipo de importacion para identificar con cython o manual
try:
    from .c_login_command import app as login  # noqa
except Exception:
    from c_login_command import app as login  # noqa

try:
    from .c_alive_command import app as alive  # noqa
except Exception:
    from c_alive_command import app as alive  # noqa

try:
    from .c_interfaces_command import app as interfaces  # noqa
except Exception:
    from c_interfaces_command import app as interfaces  # noqa

try:
    from .c_inventory_command import app as inventory  # noqa
except Exception:
    from c_inventory_command import app as inventory  # noqa


def main():
    return app()


if __name__ == "__main__":
    main()
