"""SDK to communicate with Nazca4.0 system
    To init SDK:
            sdk = SDK()
            if https is required then:
            sdk = SDK(https = True)
    To get info about system:
            sdk.modules returns list of all modules
            sdk.variables returns dictionary with key:module value: available variables
    Example:
            sdk.modules -> [Module1, Module2, ... ]
            sdk.variables ->{
                                Module_Name: [Var1, Var2, ... ]
                            }
"""

from datetime import datetime

from pydantic import ValidationError

from nazca4sdk import UserVariableInfo, UserVariable
from nazca4sdk.cache import Cache
from nazca4sdk.datahandling.cache.cache_storage import CacheStorage
from nazca4sdk.datahandling.cache.key_value import KeyValue
from nazca4sdk.datahandling.hotstorage.hot_storage import HotStorage
from nazca4sdk.datahandling.knowledge.knowledge_data_type import KnowledgeDataType
from nazca4sdk.datahandling.knowledge.knowledge_storage import KnowledgeStorage
from nazca4sdk.datahandling.nazcavariables.nazca_variables_storage import NazcaVariablesStorage
from nazca4sdk.datahandling.variable_verificator import VariableIntervalInfo, \
    VariableIntervalSubtractionInfo
from nazca4sdk.tools.time import get_time_delta


class SDK:
    """SDK by Nazca4 system"""

    def __init__(self, https: bool = True):
        """ Initializing the system, checking connection and caching system configuration
        if https is required then https = True"""

        self.__https = https
        self.__system_cache = Cache(https)
        self.__cache = CacheStorage(https)
        self.__knowledge = KnowledgeStorage(https)
        self.__hot_storage = HotStorage(https)
        self.__nazca_variables_storage = NazcaVariablesStorage(https)
        if not self.__system_cache.load:
            print("Init SDK failed")
            self.modules = []
            self.variables = []
            self.types = []
        else:
            self.modules = self.__system_cache.modules
            self.variables = self.__system_cache.variables

    def variable_over_day(self, module_name, variable_names, start_date, end_date):
        """Get variables in specific time range

        Args:
            module_name - name of module,
            variable_names - list of variable names,
            start_time - start time of data acquisition
            stop_time - end time of data acquisition

        Returns:
            DataFrame: Variable values from selected time range

        Example:
            sdk.variable_over_day('Module_Name', ['Variable1'],
                start_date = '2000-01-01T00:00:00',
                 end_date = '2000-01-01T12:00:00')
        """
        try:
            data = {'module_name': module_name,
                    'variable_names': variable_names,
                    'start_date': start_date,
                    'end_date': end_date}
            variable_info = VariableIntervalInfo(**data)
            result = self.__system_cache.variable_over_day(variable_info.module_name,
                                                           variable_info.variable_names,
                                                           variable_info.start_date,
                                                           variable_info.end_date)
            if result is None:
                return None
            return result.to_df()
        except ValidationError as error:
            print(error.json())
            return None

    def variable_over_time(self, module_name: str,
                           variable_names: list,
                           time_amount: int,
                           time_unit: str):
        """ Get variables in specific time range

        Args:
            module_name - name of module,
            variable_names - list of variable names,
            time_amount - beginning of the time range
            time_unit - 'DAY','HOUR'...

        Returns:
            DataFrame: Variable values from selected time range

        Example:
              sdk.variable_over_time('Module_Name', ['Variable1'], 10, 'MINUTE')
        """
        try:
            data = {'module_name': module_name,
                    'variable_names': variable_names,
                    'time_amount': time_amount,
                    'time_unit': time_unit}
            variable_info = VariableIntervalSubtractionInfo(**data)

            end_date = datetime.now()
            start_date = end_date - get_time_delta(time_unit, time_amount)

            result = self.__system_cache.variable_over_day(variable_info.module_name,
                                                           variable_info.variable_names,
                                                           start_date,
                                                           end_date)
            if result is None:
                return None
            return result.to_df()
        except ValidationError as error:
            print(error.json())
            return None

    def write_hotstorage_variables(self, user_variables: [UserVariable]):
        """
         Save user variables in hot storage
        Args:
            user_variables: list of user variables to save

        Returns:
            True - variables to save send to hot storage
            False - communication with hot storage error
        """
        return self.__hot_storage.save_variables(user_variables)

    def read_hotstorage_variables(self, start_date: str, end_date: str, variables: [UserVariableInfo]):
        """
        Read user variables from hot storage
        Args:
            start_date: begin of time range
            end_date: end of time range
            variables: list of user variables to read

        Returns:
            list of user variables values from hot storage
        """
        return self.__hot_storage.read_variables(start_date, end_date, variables)

    def read_cache_keys(self, keys):
        """
        Read cache values for list of keys

        Args:
            keys: List of keys to read from cache

        Returns:
            List of CacheEntry
        """
        return self.__cache.read_keys(keys)

    def write_cache_keys(self, key: str, value):
        """write key value to cache

        Args:
            key: key
            value: value to write to cache
        Returns:
            CacheEntry if success or None if error
        """

        data = {'key': key,
                'value': value}
        try:
            variable_info = KeyValue(**data)
            return self.__cache.write_keys(variable_info)
        except ValidationError as error:
            print(error.json())
            return None

    def read_knowledge(self, key: str):
        return self.__knowledge.read_key_values(key)

    def write_knowledge(self, key: str, section: str, value: str, datatype: KnowledgeDataType):
        return self.__knowledge.write_key_values(key, section, value, datatype)

    def daily_media_usage(self, module_name: str, variable_name: str):
        """ Function to calculate daily media usage like air, etc.
        Args:
            module_name - name of module,
            variable_name - desired variable,

            Returns:
                Float: Value

            Example:
                daily_media_usage('Module_Name', 'Variable_Name')
        """

        start_date = datetime.today().strftime("%Y-%m-%dT00:00:00")
        end_date = datetime.today().strftime("%Y-%m-%dT%H:%M:%S")
        try:
            data = self.variable_over_day(module_name, [variable_name], start_date=start_date, end_date=end_date)
            if data is None:
                return None
            return round(data.value.iloc[-1] - data.value.iloc[0], 2)
        except ValidationError as error:
            print(error.json())
            return None

    def daily_energy_usage(self, module_name):
        """ Function to calculate daily electric energy usage
        Args:
            module_name - name of module,

            Returns:
                Float: Value

            Example:
                daily_energy_usage('Module_Name')
        """

        start_date = datetime.today().strftime("%Y-%m-%dT00:00:00")
        end_date = datetime.today().strftime("%Y-%m-%dT%H:%M:%S")

        try:
            ea_dec = self.variable_over_day(module_name, ['Ea_dec'], start_date=start_date, end_date=end_date)
            ea_res = self.variable_over_day(module_name, ['Ea_res'], start_date=start_date, end_date=end_date)
            if (ea_dec is None) or (ea_res is None):
                return None
            energy_now = ea_dec.value.iloc[-1] + ea_res.value.iloc[-1]
            energy_previous = ea_dec.value.iloc[0] + ea_res.value.iloc[0]
            return round(energy_now - energy_previous, 2)
        except ValidationError as error:
            print(error.json())
            return None

    def read_nazca_variables(self):
        return self.__nazca_variables_storage.read_variables()

    def read_nazca_variable(self, identifier: str):
        return self.__nazca_variables_storage.read_variable(identifier)
