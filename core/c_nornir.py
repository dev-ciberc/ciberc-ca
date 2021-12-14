from nornir import InitNornir
from nornir.core.filter import F


class DevopsNornir:

    def __init__(self, path: str = None, filter: str = None, workers: int = 2):
        self.nr = InitNornir(
            logging={"log_file": "ciberc-ca.log", "level": "DEBUG"},

            runner={
                "plugin": "threaded",
                "options": {
                    "num_workers": workers,
                },
            },
            inventory={
                "plugin": 'SimpleInventory',

                "options": {
                    "host_file": f"{path}/hosts.yaml",
                    "group_file": f"{path}/groups.yaml",
                    "defaults_file": f"{path}/defaults.yaml",
                }
            },
            dry_run=True
        )

        if filter is not None:
            for group in filter.split(","):
                self.nr = self.nr.filter(F(groups__contains=group))

    def init(self):
        return self.nr
