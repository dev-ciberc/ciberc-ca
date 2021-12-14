import json
import sys

from napalm import get_network_driver
from nornir.core.task import Result, Task
from tqdm import tqdm
from ttp import ttp

try:
    from .c_nornir import DevopsNornir
except Exception:
    from c_nornir import DevopsNornir

try:
    from .c_templates import StringTemplates
except Exception:
    from c_templates import StringTemplates

try:
    from .c_interfaces_excel import ExcelInterfaces
except Exception:
    from c_interfaces_excel import ExcelInterfaces

try:
    from .c_login import Login
except Exception:
    from c_login import Login


class Interfaces:

    def __init__(self, path: str = None, filter: str = None, workers: int = 1):
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
        self.template = StringTemplates()
        self.exclude = -1

        login = Login()
        if login.validateToken() is False:
            raise Exception("Login failed")

    def update_pbar(self):
        self.pbar.update(self.up)
        self.pbar.refresh()
        sys.stdout.flush()

    def data_json(self):
        data = json.dumps(self.data, indent=self.indent,
                          sort_keys=self.sort_keys)
        return data

    def data_excel(self, mechanism, name):
        try:
            excel = ExcelInterfaces()
            excel.create(self.data, mechanism)
            excel.save(name)
        except Exception:
            return False

        return True

    def get_interfaces(self, device):
        dict_interfaces = device.get_interfaces()
        filtrado = {}

        if len(dict_interfaces) > 0:
            # filtrado de interfaces solo activas
            filtrado = dict(
                filter(lambda i: i[1]['is_up'] is True, dict_interfaces.items()))  # noqa

            filtrado = dict(filter(
                lambda i: i[0].find('Vlan') == self.exclude
                and i[0].find('Loop') == self.exclude
                and i[0].find('Tu') == self.exclude, filtrado.items()
            ))

        return filtrado

    def get_services(self, device, interfaces_filtered):
        data = interfaces_filtered.copy()

        if len(interfaces_filtered) > 0:
            for key, value in interfaces_filtered.items():
                comando = f"show run interface {key}"
                interface_data = device.cli([comando])

                try:
                    string_services = interface_data[comando]
                    parser = ttp(data=string_services,
                                 template=self.template.get_ttp_services())
                    parser.parse()
                except Exception:
                    pass

                try:
                    services_per_interface = parser.result()[0][0]['services']
                except Exception:
                    # si la interface es modo trocal
                    # get_ttp_trunk
                    try:
                        string_services = interface_data[comando]
                        parser = ttp(data=string_services,
                                     template=self.template.get_ttp_trunk())
                        parser.parse()
                    except Exception:
                        pass

                    try:
                        services_per_interface = parser.result()[0][0]['services']  # noqa
                    except Exception:
                        services_per_interface = {}

                data[key]['services'] = services_per_interface

        return data

    def get_vlan(self, device, data):

        for item in data:
            # recorre por cada interface los servicios
            try:
                services_list = [data[item]["services"]] if data[item]["services"].__class__ == dict else data[item]["services"]  # noqa
            except Exception:
                services_list = []

            if len(services_list) != 0:
                for service in services_list:
                    # validar si es trunk
                    # service_instance en el item
                    if 'service_instance' in service:

                        # verificar vlans para las interfaces troncales

                        try:

                            vlans_list = service['data']['switchport_vlans']
                            service['vlan'] = list([])

                            for vl in vlans_list:
                                try:
                                    comando_vlan = f"show run interface vlan {vl}"  # noqa
                                    dato_vlan = device.cli([comando_vlan])
                                    string_vlan = dato_vlan[comando_vlan]

                                    parser_vlan = ttp(data=string_vlan, template=self.template.get_ttp_vlan())  # noqa
                                    parser_vlan.parse()
                                except Exception:
                                    # el servicio no tiene vlans configuradas
                                    pass

                                try:
                                    vlan_per_servicio = parser_vlan.result()[0][0]['interface_vlan']  # noqa
                                except Exception:
                                    vlan_per_servicio = {}

                                service['vlan'].append(vlan_per_servicio)  # noqa

                        except Exception:
                            # interfaces que poseen servicios

                            try:
                                comando_vlan = f"show run interface vlan {service['service_instance']}"  # noqa
                                dato_vlan = device.cli([comando_vlan])
                                string_vlan = dato_vlan[comando_vlan]

                                parser_vlan = ttp(data=string_vlan, template=self.template.get_ttp_vlan())  # noqa
                                parser_vlan.parse()
                            except Exception:
                                # el servicio no tiene vlans configuradas
                                pass

                            try:
                                vlan_per_servicio = parser_vlan.result()[0][0]['interface_vlan']  # noqa
                            except Exception:
                                vlan_per_servicio = {}

                            service['vlan'] = [vlan_per_servicio]  # noqa

        return data

    def get_validacion_vlans(self, device, data):

        for item in data:
            # recorre por cada interface los servicios
            try:
                services_list = [data[item]["services"]] if data[item]["services"].__class__ == dict else data[item]["services"]  # noqa
            except Exception:
                services_list = []

            # se recorren los servicios por cada interface
            for service in services_list:
                try:
                    vlans_list = [service['vlan']] if service['vlan'].__class__ == dict else service['vlan']  # noqa
                except Exception:
                    vlans_list = []

                # ser recorren las vlans de cada servicio
                for vlan in vlans_list:
                    # bridge domain
                    bridge_domain = service["service_instance"]

                    # --
                    # -- primer comando para optener las interfaces bridge
                    # --
                    try:
                        comando_bridge = f"show bridge-domain {bridge_domain}"  # noqa
                        int_valn = device.cli([comando_bridge])
                        string_vlan = int_valn[comando_bridge]

                        parse = ttp(data=string_vlan, template=self.template.get_ttp_bridge())  # noqa
                        parse.parse()
                    except Exception:
                        pass

                    try:
                        int_bridges = parse.result()[0][0]['bridges']  # noqa
                    except Exception:
                        int_bridges = {}

                    # asignacion de las interfaces bridge_domain a la vlan
                    vlan['bridges'] = int_bridges

                    cant_bridges = 0
                    if len(int_bridges) > 0:
                        cant_bridges = len(
                            int_bridges['interfaces']) if int_bridges['interfaces'].__class__ == list else 1 if int_bridges != {} else 0  # noqa
                    vlan['cant_bridges'] = cant_bridges

                    # --
                    # -- segundo comando para optener los puertos
                    # --
                    try:
                        comando_bridge = f"show mac-address-table dynamic vlan {bridge_domain}"  # noqa
                        ports_vlan = device.cli([comando_bridge])
                        string_vlan = ports_vlan[comando_bridge]

                        parse_dyn = ttp(data=string_vlan, template=self.template.get_ttp_ports())  # noqa
                        parse_dyn.parse()
                    except Exception:
                        pass

                    try:
                        ports = parse_dyn.result()[0][0]['ports']  # noqa
                    except Exception:
                        ports = {}

                    # asignacion de las puertos de la vlan
                    vlan['ports'] = ports
                    vlan['cant_ports'] = len(ports) if ports.__class__ == list else 1 if ports != {} else 0  # noqa

        return data

    def execute(self, task: Task):
        try:
            driver = get_network_driver(task.host.platform)

            device = driver(
                hostname=task.host.hostname,
                username=task.host.username,
                password=task.host.password,
                timeout=10,
                optional_args={'port': task.host.port},
            )

            # [paso 01] apertura de la unica sesion por equipo
            device.open()

            # [paso 02] recolectar todas las interfaces del equipo
            datos_interfaces = self.get_interfaces(device)

            # [paso 03] recolectar todas las interfaces del equipo los servicios # noqa
            datos_interfaces = self.get_services(device, datos_interfaces)

            # [paso 04] recolectar todas las interfaces del equipo por servicio las vlan # noqa
            datos_interfaces = self.get_vlan(device, datos_interfaces)

            # [paso 05] recoletar por cada vlan de los servicios
            # las validaciones correspondientes
            datos_interfaces = self.get_validacion_vlans(device, datos_interfaces)  # noqa

            # validar conexion del dispositivo
            result = Result(
                host=task.host,
                result=datos_interfaces
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
                name="interfaces",
                task=self.execute,
            )

            self.pbar.close()

            for item in result:
                try:
                    data = result[item][0].result
                except Exception:
                    data = {}
                dict_result[item] = data

        self.data = dict_result

        return dict_result
