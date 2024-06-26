
try:
    from .c_typer import app
except Exception:
    from .c_typer import app


# tipo de importacion para identificar con python o manual
try:
    from .c_alive_command import app as alive  # noqa
except Exception:
    from .c_alive_command import app as alive  # noqa

try:
    from .c_interfaces_command import app as interfaces  # noqa
except Exception:
    from .c_interfaces_command import app as interfaces  # noqa

try:
    from .c_inventory_command import app as inventory  # noqa
except Exception:
    from .c_inventory_command import app as inventory  # noqa

try:
    from .c_ping_command import app as ping  # noqa
except Exception:
    from .c_ping_command import app as ping  # noqa

try:
    from .c_merge_ping_command import app as ping_merge  # noqa
except Exception:
    from .c_merge_ping_command import app as ping_merge  # noqa

try:
    from .c_records_command import app as records  # noqa
except Exception:
    from .c_records_command import app as records  # noqa


def main():
    return app()


if __name__ == "__main__":
    main()
