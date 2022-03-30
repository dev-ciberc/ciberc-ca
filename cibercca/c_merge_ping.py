import json
import os

import pandas as pd


class PingMerge:
    def __init__(self, file_src, file_dst) -> None:
        # --
        # final dataframe compared and validated
        self.data = None

        # --
        # contains the upload data of the files
        self.file_src = file_src
        self.file_dst = file_dst
        self.data_src = None
        self.data_dst = None
        self.file_src_ext = None
        self.file_dst_ext = None

        # --
        # dataframe with the source vrf
        self.df_source = None

        # --
        # dataframe with the destination vrf
        self.df_dest = None

        # --
        # columns for dataframe report baseline ping
        self.columnsDataFrame = [
            "src_device",
            "src_ip_address",
            "src_vrf",
            "src_interface",
            "src_mac",
            "src_interface_ip_address",
            "dst_device",
            "dst_ip_address",
            "dst_vrf",
            "dst_interface",
            "dst_mac",
            "dst_interface_ip_address",
            "initial_ping_percent",
            "final_ping_percent",
            "status"
        ]

        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # --
    # load the files, source and destination
    def loadFiles(self) -> None:
        """
        load the files, source and destination

        file_src: the source file vrf listing
        file_dst: the destination file vrf listing
        """

        # --
        # load file source and identifier extension
        file = open(self.file_src)
        self.file_src_ext = os.path.splitext(self.file_src)[1]

        if self.file_src_ext == '.json':
            self.data_src = json.load(file)
        else:
            self.data_src = pd.read_excel(self.file_src)

        # --
        # load file destination and identifier extension
        file_dst = open(self.file_dst)
        self.file_dst_ext = os.path.splitext(self.file_dst)[1]

        if self.file_dst_ext == '.json':
            self.data_dst = json.load(file_dst)
        else:
            self.data_dst = pd.read_excel(self.file_dst)

    def json_to_dataframe(self, data):
        """
        json_to_dataframe:

        data: the json data with the vrfs list

        transform the json data to a dataframe
        """

        columns = [
            "device",
            "source",
            "ip_address",
            "vrf",
            "interface",
            "mac",
            "interface_ip_address",
            "percent"
        ]

        final_list = []

        for key in data:
            device = data[key]['data']

            EC_DEVICE_NAME = device['name']
            EC_DEVICE_HOSTNAME = device['hostname']

            try:
                EC_SOURCE = device['source']
            except Exception:
                EC_SOURCE = ''

            # --
            # listar las vrfs asignadas al equipo origen
            # --

            for vrf in device['list_vrf']:
                EC_VRF_NAME = vrf['vrf_name']

                if len(vrf['ips_arp']) > 0:
                    for ip in vrf["ips_arp"]:
                        EC_VRF_INTERFACE = ip['interface']
                        EC_VRF_MAC_ADDRESS = ip['mac']
                        EC_VRF_IP_ADDRESS = ip['ip_address']

                        try:
                            EC_VRF_PERCENT = ip["ping_arp"][0]['percent']
                        except Exception:
                            EC_VRF_PERCENT = ""

                        row = [
                            EC_DEVICE_NAME,
                            EC_SOURCE,
                            EC_DEVICE_HOSTNAME,
                            EC_VRF_NAME,
                            EC_VRF_INTERFACE,
                            EC_VRF_MAC_ADDRESS,
                            EC_VRF_IP_ADDRESS,
                            EC_VRF_PERCENT
                        ]
                        final_list.append(row)

                else:
                    row = [EC_DEVICE_NAME, EC_SOURCE,
                           EC_DEVICE_HOSTNAME, EC_VRF_NAME, "", "", "", ""]
                    final_list.append(row)

            # --
            # si el dispositivo no tiene vrfs asignadas
            if len(device['list_vrf']) == 0:
                row = [EC_DEVICE_NAME, EC_SOURCE,
                       EC_DEVICE_HOSTNAME, "", "", "", "", ""]
                final_list.append(row)

        return pd.DataFrame(final_list, columns=columns)

    def excel_to_dataframe(self, data):
        final_list = []

        columns = [
            "device",
            "source",
            "ip_address",
            "vrf",
            "interface",
            "mac",
            "interface_ip_address",
            "percent"
        ]

        for row in data.itertuples():
            EC_DEVICE_NAME = row[1]
            EC_SOURCE = row[2]
            EC_DEVICE_HOSTNAME = row[3]
            EC_VRF_NAME = row[4]
            EC_VRF_INTERFACE = row[5]
            EC_VRF_MAC_ADDRESS = row[6]
            EC_VRF_IP_ADDRESS = row[7]
            EC_VRF_PERCENT = row[8]

            row = [
                EC_DEVICE_NAME,
                EC_SOURCE,
                EC_DEVICE_HOSTNAME,
                EC_VRF_NAME,
                EC_VRF_INTERFACE,
                EC_VRF_MAC_ADDRESS,
                EC_VRF_IP_ADDRESS,
                EC_VRF_PERCENT
            ]
            final_list.append(row)

        return pd.DataFrame(final_list, columns=columns)

    # --
    # return the data json/excel vrf to dataframe

    def transform(self, data, ext):
        if ext == ".json":
            return self.json_to_dataframe(data)
        else:
            return self.excel_to_dataframe(data)

    def createDataframeSourceOnly(self, origin, dest_device):
        """
        createDataframeSourceOnly:

        origin: the source device vrfs list
        dest_device: the destination device vrfs list

        when the source is validated against the
        destination and exists only in the source
        """  # noqa
        df = pd.DataFrame(
            [
                [
                    origin.device,
                    origin.ip_address,
                    origin.vrf,
                    origin.interface,
                    origin.mac,
                    origin.interface_ip_address,
                    dest_device,
                    "",
                    "",
                    "",
                    "",
                    "",
                    int(origin.percent),
                    0,
                    origin.validate
                ]
            ],
            columns=self.columnsDataFrame
        )

        return df

    def createDataframeSourceDest(self, origin, dest):
        """
        createDataframeSourceDest:

        origin: the source device vrfs list
        dest_device: the destination device vrfs list

        when the destination is validated with the origin and both are found,
        the ping percentage is validated
        """  # noqa
        df = pd.DataFrame(
            [
                [
                    origin.device.values[0],
                    origin.ip_address.values[0],
                    origin.vrf.values[0],
                    origin.interface.values[0],
                    origin.mac.values[0],
                    origin.interface_ip_address.values[0],
                    dest.device,
                    dest.ip_address,
                    dest.vrf,
                    dest.interface,
                    dest.mac,
                    dest.interface_ip_address,
                    int(origin.percent),
                    int(dest.percent),
                    dest.validate
                ]
            ],
            columns=self.columnsDataFrame
        )

        return df

    def createDataframeDestNew(self, dest, source_device):
        """
        createDataframeDestNew:

        origin: the source device vrfs list
        dest_device: the destination device vrfs list

        when the destination vrf does not exist in the source device,
        it is cataloged as new
        """  # noqa
        df = pd.DataFrame(
            [
                [
                    source_device,
                    '',
                    '',
                    '',
                    '',
                    '',
                    dest.device,
                    dest.ip_address,
                    dest.vrf,
                    dest.interface,
                    dest.mac,
                    dest.interface_ip_address,
                    0,
                    int(dest.percent),
                    dest.validate
                ]
            ],
            columns=self.columnsDataFrame
        )

        return df

    def compareVrfs(self, dest, source) -> pd.DataFrame():
        # --
        # data frame que contendra la nueva estructura del reporte final baseline ping # noqa
        data = pd.DataFrame(
            columns=self.columnsDataFrame
        )

        # --
        # lista de dispositivos agrupados por device, source
        distinct_devices = \
            dest.groupby(['device', 'source'])['device'].count()

        for row in distinct_devices.index:
            device = row[0]
            source_device = row[1]

            # --
            # se filtran solo las vrfs del dispositivo origen
            list_source_filter = source.loc[source['device'] == source_device]

            # --
            # se filtran solo las vrfs del dispositivo destino
            list_dst_filter = dest.loc[dest['device'] == device]

            # --
            # listado de vrf del dispositivo destino
            list_unique_vrf_dst = list_dst_filter['vrf'].unique()

            # --
            # listado de vrf del dispositivo origen
            list_unique_vrf_src = list_source_filter['vrf'].unique()

            # --
            # listado completo de las vrfs de los dispositivos
            union_vrfs = \
                (set((list(list_unique_vrf_src) + list(list_unique_vrf_dst))))

            # --
            # las vrf que solo existen en el destino son categorizadas [nuevas = NEW] # noqa
            # las vrf que existen en origen, destino con los mismos parametros con [OK] # noqa
            # las vrf que existen en origin, destino con diferentes parametros con [FAIL] # noqa
            for vrf in union_vrfs:
                # --
                # segun la vrf unica del destino se filtra la vrf del origen # noqa
                list_vrf_source = list_source_filter.loc[list_source_filter['vrf'] == vrf]  # noqa

                # --
                # segun la vrf unica del destino se filtra su propio dispositivo # noqa
                list_vrf_dest = list_dst_filter.loc[list_dst_filter['vrf'] == vrf]  # noqa

                # --
                # se buscan las vrf destino en el origen
                for _, item in list_vrf_dest.iterrows():
                    vrf_item_source = list_vrf_source.loc[
                        (list_vrf_source['vrf'] == item.vrf)
                        & (list_vrf_source['interface'] == item.interface)
                        & (list_vrf_source['interface_ip_address'] == item.interface_ip_address)  # noqa
                    ]  # noqa

                    if vrf_item_source.empty:  # noqa
                        item['validate'] = 'NEW'
                        try:
                            data = pd.concat(
                                [data, self.createDataframeDestNew(item, source_device)])  # noqa
                        except Exception:
                            # si no hay datos en ambos data frame no es valido el # noqa
                            # catalogado como new (vacio)
                            pass
                    else:
                        if item.percent >= vrf_item_source.percent.values[0]:
                            item['validate'] = 'OK'
                        else:
                            item['validate'] = 'FAIL'

                        # se crea dataframe con la vrf destino, como la origen
                        data = pd.concat(
                            [data, self.createDataframeSourceDest(vrf_item_source, item)])  # noqa

            # --
            # El ultimo proceso es buscar todas las vrf origin que no existan en destino # noqa
            for vrf_source in list_unique_vrf_src:
                # --
                # segun la vrf unica del origin se filtra asi misma
                list_vrf_source = \
                    list_source_filter.loc[list_source_filter['vrf']
                                           == vrf_source]

                # --
                # segun la vrf unica del origen se filtran las destino
                list_vrf_dest = list_dst_filter.loc[list_dst_filter['vrf'] == vrf_source]  # noqa

                # --
                # se buscan las vrf origen para que no existan en el destino
                for _, item in list_vrf_source.iterrows():
                    vrf_item = list_vrf_dest.loc[
                        (list_vrf_dest['vrf'] == item.vrf)
                        & (list_vrf_dest['interface'] == item.interface)
                        & (list_vrf_dest['interface_ip_address'] == item.interface_ip_address)  # noqa
                    ]  # noqa

                    if vrf_item.empty:  # noqa
                        item['validate'] = 'FAIL'
                        data = pd.concat(
                            [data, self.createDataframeSourceOnly(item, device)])  # noqa

        return data

    def data_json(self):
        # --
        # se transforma el dataframe en un json
        self.data.to_json(f'reporte_vrf.json', orient='records')  # noqa
        return self.data

    def data_excel(self, file_name):
        # --
        # se transforma el dataframe en un excel
        try:
            self.data.to_excel(f'{file_name}.xlsx', index=False)
        except Exception:
            return False

        return True

    def run(self) -> None:
        # --
        # load the files, to precess
        self.loadFiles()

        # --
        # transform the json vrf source to dataframe
        self.df_source = self.transform(self.data_src, self.file_src_ext)

        # --
        # transform the json vrf destination to dataframe
        self.df_dest = self.transform(self.data_dst, self.file_dst_ext)

        # --
        # compare the vrfs
        self.data = self.compareVrfs(self.df_dest, self.df_source)
