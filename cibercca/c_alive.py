import json
import sys

from napalm import get_network_driver
from nornir.core.task import Result, Task
from tabulate import tabulate
from tqdm import tqdm

from .c_database import db_conecction
from .data_cibercca import Data_cibercca
from datetime import datetime
from flask import jsonify

try:
    from .c_nornir import DevopsNornir
except Exception:
    from .c_nornir import DevopsNornir

try:
    from .c_nornir import DevopsNornir
except Exception:
    from .c_nornir import DevopsNornir


class Alive:

    def __init__(self, path: str = None, filter: str = None, workers: int = 2):
        nornir = DevopsNornir(path=path, filter=filter, workers=workers)
        self.nr = nornir.init()
        self.n_devices = len(self.nr.inventory.hosts.keys())
        try:
            self.equitativo = int(100 / int(self.n_devices))
        except Exception:
            self.equitativo = 100
        self.up = self.equitativo if self.equitativo % 2 == 0 else self.equitativo + 1  # noqa
        self.indent = 3
        self.sort_keys = True
        self.data = None

    def update_pbar(self):
        self.pbar.update(self.up)
        self.pbar.refresh()
        sys.stdout.flush()

    def data_json(self):
        data = json.dumps(self.data, indent=self.indent,
                          sort_keys=self.sort_keys)
        return data

    def data_table(self):
        array_for_tabulate = [['name', 'is_alive']]
        for item in self.data:
            try:
                array_for_tabulate.append(
                    [item, self.data[item]['data']['is_alive']])
            except Exception:
                pass
        data = (tabulate(array_for_tabulate, headers='firstrow', tablefmt='grid'))  # noqa
        return data
    
    def data_database(self):
 
        data_save = json.dumps(self.data, indent=self.indent,
                          sort_keys=self.sort_keys)

        response = Alive.add_data(data_save)

        print(response)

    def _alive(self, task: Task):
        try:
            driver = get_network_driver(task.host.platform)

            device = driver(
                hostname=task.host.hostname,
                username=task.host.username,
                password=task.host.password,
                optional_args={'port': task.host.port},
            )

            try:
                device.open()
            except Exception:
                try:
                    device.open()
                except Exception:
                    device.open()

            result = Result(
                host=task.host,
                result=device.is_alive()
            )

            device.close()

        except Exception as e:
            try:
                device.close()
            except Exception:
                pass

            result = Result(
                host=task.host,
                result={"error": str(e)}
            )

        self.update_pbar()

        return result
    
    def run(self):
        dict_result = {}

        # solo si hay dispositivos en el inventario
        if self.n_devices > 0:
            self.pbar = tqdm(total=100)

            result = self.nr.run(
                name="alive",
                task=self._alive,
            )

            self.pbar.close()

            for item in result:
                dict_result[item] = {"data": result[item][0].result}

        self.data = dict_result

        return dict_result

    
    def add_data(self):
        db = db_conecction()

        info = db["db_cibercca"]
        command = 'alive'
        date =  datetime.now()
        data_from_device = self

        if command and date and data_from_device:
                item = Data_cibercca(command, date,data_from_device)
                info.insert_one(item.toDBCollection())
                response = jsonify({
                    'command' : command,
                    'date' : date,
                    'data_from_device': data_from_device
                })
                
                return response
        else:
                return print('Data could not be saved. Please, verify database connection.')