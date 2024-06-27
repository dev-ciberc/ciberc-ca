class DataCibercca:
    def __init__(self, command,date,data_from_device):
        self.command = command
        self.date = date
        self.data_from_device = data_from_device

    def to_db_collection(self):
        return{
            'command': self.command,
            'date': self.date,
            'data_from_device': self.data_from_device
        } 