# clase para listado de vrf destino de la migracion
import json
import sys

from netmiko import ConnectHandler
from nornir.core.task import Result, Task
# from tabulate import tabulate
from tqdm import tqdm
from ttp import ttp

try:
    from .c_nornir import DevopsNornir
except Exception:
    from c_nornir import DevopsNornir

try:
    from .c_ping_dst_excel import ExcelVrfDestination
except Exception:
    from c_ping_dst_excel import ExcelVrfDestination  # noqa

try:
    from .c_templates import StringTemplates
except Exception:
    from c_templates import StringTemplates


class DestinationNetwork():

    def __init__(self, path: str = None, filter: str = None, workers: int = 2):
        nornir = DevopsNornir(path=path, filter=filter, workers=workers)
        self.nr = nornir.init()
        self.n_devices = len(self.nr.inventory.hosts.keys())
        self.template = StringTemplates()

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

    def data_excel(self, name):
        try:
            excel = ExcelVrfDestination()
            excel.create(self.data)
            excel.save(name)
        except Exception:
            return False

        return True

    def data_table(self) -> list:
        # data = (tabulate(array_for_tabulate, headers='firstrow', tablefmt='grid'))  # noqa
        return []

    def get_vrf(self, device) -> list:

        result = []

        try:
            comando = "show vrf all | ex import | ex export"
            dato_cli = device.send_command(comando)
            parser = ttp(data=dato_cli,
                         template=self.template.get_ttp_vrf_dst())
            parser.parse()
            result = parser.result()[0][0]
        except Exception:
            pass

        return result

    def get_ip_arp_vrf(self, device, datos):

        for dato in datos:
            ips_arp = {}
            try:
                comando = f"show arp vrf {dato['vrf_name']} | i Dynamic"  # noqa
                dato_cli = device.send_command(comando)
                parser = ttp(data=dato_cli,
                             template=self.template.get_ttp_arp_vrf_dst())
                parser.parse()
                ips_arp = parser.result()[0][0]
            except Exception as e:
                print(f"error arp vrf: {e}")

            dato['ips_arp'] = ips_arp

        return datos

    def get_ping_ip_arp_vrf(self, device, datos):

        for vrf in datos:
            try:
                ips_arp = vrf['ips_arp']
            except Exception:
                ips_arp = []

            for ip in ips_arp:

                ping_arp = {}
                try:
                    comando = f"ping vrf {vrf['vrf_name']} {ip['ip_address']} count 4"  # noqa
                    dato_cli = device.send_command(comando)
                    parser = ttp(data=dato_cli,
                                 template=self.template.get_ttp_ping_ip_arp())
                    parser.parse()
                    ping_arp = parser.result()[0][0]
                except Exception:
                    pass

                ip['ping_arp'] = ping_arp

        return datos

    def ping_dst(self, task: Task):
        try:
            platform = "cisco_xr" if task.host.platform == "iosxr" else task.host.platform  # noqa
            host = {
                "ip": task.host.hostname,
                "username": task.host.username,
                "password": task.host.password,
                'port': task.host.port,
                "device_type": platform,
            }

            # [paso 01] apertura de la unica sesion por equipo
            try:
                device = ConnectHandler(**host)
            except Exception:
                try:
                    device = ConnectHandler(**host)
                except Exception:
                    device = ConnectHandler(**host)

            # [paso 02] se optiene una lista de las vrf del equipo con
            # las interfaces asignadas
            datos = self.get_vrf(device)

            # [paso 03] por cada vrf se lista la tabla de arp vrf
            datos = self.get_ip_arp_vrf(device, datos)

            # [paso 04] por cada ip se realiza un ping
            datos = self.get_ping_ip_arp_vrf(device, datos)

            result = Result(
                host=task.host,
                result={
                    "name": task.host.name,
                    "hostname": task.host.hostname,
                    "platform": task.host.platform,
                    "source": task.host["source"],
                    "list_vrf": datos
                },
            )

        except Exception as e:
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
                name="ping destination",
                task=self.ping_dst,
            )

            self.pbar.close()

            for item in result:
                dict_result[item] = {"data": result[item][0].result}

        self.data = dict_result

        return dict_result
