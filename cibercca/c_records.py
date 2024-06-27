import json

from .c_database import db_conecction as dbase


class Records:

    def find_data(self):
        try:
            db = dbase()

            info = db["db_cibercca"]

            # Apply filter for data         
            _filter = {'command': str(self)}
            info_received = list(info.find(_filter))

            for item in info_received:
                if '_id' in item:
                    item['data_from_device'] = json.loads(item['data_from_device'])
                    del item['_id']

            documentos_json = json.dumps(info_received, default=str, indent=4)

            return documentos_json

        except FileNotFoundError: 
            return print('Do not exist data in Database')
