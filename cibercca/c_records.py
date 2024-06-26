import json
import sys

from napalm import get_network_driver
from nornir.core.task import Result, Task
from tabulate import tabulate
from tqdm import tqdm

from .c_database import db_conecction as dbase


class Records:

    def findData(command):
        try:
            db = dbase()

            info = db["db_cibercca"]

            # Apply filter for data         
            filter = {'command': str(command)}
            infoReceived = list(info.find(filter))

            for item in infoReceived:
                if '_id' in item:
                    item['data_from_device'] = json.loads(item['data_from_device'])
                    del item['_id']

            documentos_json = json.dumps(infoReceived, default=str, indent=4)

            return documentos_json

        except:
            return print('Do not exist data in Database')
