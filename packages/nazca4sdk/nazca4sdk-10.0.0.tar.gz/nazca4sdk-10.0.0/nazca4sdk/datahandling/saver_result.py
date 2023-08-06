"""Save result module"""
from datetime import datetime, date
from clickhouse_driver import Client


class Save:
    """Temporary class to save data to CH"""

    def __init__(self):
        self.host = '10.217.1.201'
        self.port = 9990
        self.user = 'click'
        self.password = 'VfA2byM0VXnpUBU9'
        self.database = 'nazca'
        self.measure_date = str(date.today())
        self.measure_time = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        self.date = datetime.now()

        self.client = Client(host=self.host,
                             port=self.port,
                             user=self.user,
                             password=self.password,
                             database=self.database)

    def __execute(self, query):
        """ Execute query on CH"""
        return self.client.execute(query)

    @staticmethod
    def __insert_data(module, measure_time, measure_date, variable, value):
        return f''' INSERT INTO nazca.devices_data_float (Module, MeasureTime,
        MeasureDate, Variable, Value)
        VALUES ('{module}', '{measure_time}', '{measure_date}', '{variable}', '{value}') '''

    def save_to_hs(self, module: str, variable: str, value: float):
        """save variable value to CH """

        return self.__execute(self.__insert_data(module, self.measure_time, self.measure_date,
                                                 variable, value))
