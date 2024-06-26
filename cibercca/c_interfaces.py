import json
import sys

from napalm import get_network_driver
from netmiko import ConnectHandler
from nornir.core.task import Result, Task
from tqdm import tqdm
from ttp import ttp

from .c_database import db_conecction
from .data_cibercca import Data_cibercca
from datetime import datetime
from flask import jsonify


try:
    from .c_nornir import DevopsNornir
except Exception:
    from .c_nornir import DevopsNornir

try:
    from .c_templates import StringTemplates
except Exception:
    from .c_templates import StringTemplates

try:
    from .c_interfaces_excel import ExcelInterfaces
except Exception:
    from .c_interfaces_excel import ExcelInterfaces


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

    def update_pbar(self):
        self.pbar.update(self.up)
        self.pbar.refresh()
        sys.stdout.flush()

    def data_json(self):
        data = json.dumps(self.data, indent=self.indent,
                          sort_keys=self.sort_keys)
        return data

    def data_database(self):
 
        data_save = json.dumps(self.data, indent=self.indent,
                          sort_keys=self.sort_keys)

        Interfaces.add_data(data_save)

    def add_data(self):
        db = db_conecction()

        info = db["db_cibercca"]
        command = 'interfaces'
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


    def data_excel(self, mechanism, name):
        try:
            excel = ExcelInterfaces()
            excel.create(self.data, mechanism)
            excel.save(name)
        except Exception:
            return False

        return True

    def get_interfaces(self, con):
        # dict_interfaces = device.get_interfaces()
        comando = "show interfaces description | i up"
        out = con.send_command(comando, delay_factor=10)
        try:
            out += con.read_until_prompt()
        except Exception:
            pass

        # --
        # -- parsear informacion de interfaces
        parser = ttp(data=out, template=self.template.get_ttp_template_interfaces_descriptions())  # noqa
        parser.parse()
        list_interfaces = parser.result()[0][0]

        filtrado = {}
        list_interfaces = (list_interfaces["interfaces"])

        filtrado = list(
            filter(lambda x: x["state"].strip() == "up", list_interfaces))

        filtrado = list(filter(
            lambda i: i["interface"].find('Vl') == -1
            and i["interface"].find('Lo') == -1
            and i["interface"].find('Tu') == -1, filtrado
        ))

        # --
        # -- segundo comando para ejecucion de las descripciones mas completas
        # para la estrutura final
        final_data_struct = {}

        # [paso 02] por cada interface obtener su descripcion
        for interface in filtrado:
            interface_name = interface["interface"]
            try:
                comando = "show interfaces " + interface_name
                out2 = con.send_command(comando, delay_factor=10)
            except Exception as e:
                print("error en comando: " + str(e))

            try:
                out2 += con.read_until_prompt()
            except Exception:
                pass

            try:
                # parseo de informacion por interface
                parser = ttp(data=out2,
                             template=self.template.get_ttp_template_interaces_data())  # noqa
                parser.parse()
                interface_data = parser.result()[0][0][0]

                print(interface_data)

                # generacion de la estrutura final

                try:
                    INTERFACE_NAME = interface_data["name"].strip()
                except Exception:
                    INTERFACE_NAME = None

                try:
                    INTERFACE_STATE = interface["state"].strip()
                except Exception:
                    INTERFACE_STATE = None

                try:
                    INTERFACE_PROTOCOL = interface["protocol"].strip()
                except Exception:
                    INTERFACE_PROTOCOL = None

                try:
                    INTERFACE_DESCRIPTION = interface["description"].strip()
                except Exception:
                    INTERFACE_DESCRIPTION = None

                try:
                    INT_MAC_ADDRESS = interface_data["hardware"]["mac_address"].strip()  # noqa
                except Exception:
                    INT_MAC_ADDRESS = None

                try:
                    INT_TYPE_HARDWARE = interface_data["hardware"]["type_hardware"].strip()  # noqa
                except Exception:
                    INT_TYPE_HARDWARE = None

                try:
                    INT_MTU = interface_data["mtu"]["mtu"].strip()  # noqa
                except Exception:
                    INT_MTU = None

                try:
                    INT_SPEED = interface_data["mtu"]["dly"].strip()  # noqa
                except Exception:
                    INT_SPEED = None

                final_data_struct[INTERFACE_NAME] = {
                    "description": INTERFACE_DESCRIPTION,
                    "is_up": INTERFACE_STATE,
                    "is_enabled": INTERFACE_PROTOCOL,
                    "mtu": INT_MTU,
                    "speed": INT_SPEED,
                    "mac_address": INT_MAC_ADDRESS,
                    "type_hardware": INT_TYPE_HARDWARE,
                }
            except Exception:
                pass

        return final_data_struct

    def get_services(self, device, interfaces_filtered):
        data = interfaces_filtered.copy()

        if len(interfaces_filtered) > 0:
            for key, value in interfaces_filtered.items():
                comando = f"show run interface {key}"

                print(key)
                interface_data = device.cli([comando])

                try:
                    string_services = interface_data[comando]
                    parser = ttp(data=string_services,
                                 template=self.template.get_ttp_services())
                    parser.parse()
                except Exception as e:
                    print(f"error parse (get_ttp_services): {e}")

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
                    except Exception as e:
                        print(f"error parse (get_ttp_trunk): {e}")

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
            # primera etapa con netmiko
            platform = "cisco_ios" if task.host.platform == "ios" else task.host.platform  # noqa
            host = {
                "ip": task.host.hostname,
                "username": task.host.username,
                "password": task.host.password,
                'port': task.host.port,
                "device_type": platform,
            }

            # [paso 01] apertura de la unica sesion por equipo
            try:
                device_with_netmiko = ConnectHandler(**host)
            except Exception:
                try:
                    device_with_netmiko = ConnectHandler(**host)
                except Exception:
                    device_with_netmiko = ConnectHandler(**host)

            # recolectar todas las interfaces del equipo
            datos_interfaces = self.get_interfaces(device_with_netmiko)
            # cierre de netmiko
            device_with_netmiko.disconnect()

            # segunda etapa con napalm
            # [paso 02] apertura de la unica sesion por equipo
            driver = get_network_driver(task.host.platform)

            # conexion con napalm
            device = driver(
                hostname=task.host.hostname,
                username=task.host.username,
                password=task.host.password,
                timeout=10,
                optional_args={'port': task.host.port},
            )

            # tres intentos de connexion
            try:
                device.open()
            except Exception:
                try:
                    device.open()
                except Exception:
                    device.open()

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

            try:
                device_with_netmiko.disconnect()
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
