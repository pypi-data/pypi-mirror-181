"""Cache module"""
import json

import requests

from nazca4sdk.datahandling.open_data_client import OpenDataClient

JSON_HEADERS = {'Content-Type': 'application/json', 'Accept': 'application/json'}


class Cache:
    """
    System caching module to as a second layer of opendata with SDK
    """

    types_dict = {"IntegerT": "int", "Float32T": "float", "TimeT": "datetime",
                  "BooleanT": "bool", "StringT": "string"}

    def __init__(self, https: bool = True):
        """
        Initializing opendata with HotStorage to receive system configuration

        """
        self.__opendata = OpenDataClient(https)
        self.__base_url = self.__opendata.base_url
        self.modules = []
        self.variables = {}
        self.types = {}

    @property
    def load(self):
        """
        Loading definitions of modules and variables

        Returns:
            list: module_name list
            list: variable_name list

        """
        try:
            response = requests.get(f'{self.__base_url}/api/Config/modulesDefinitions', verify=False)
            if response.status_code == 200:
                json_response = response.json()
                for element in json_response:
                    module = element['identifier']
                    self.modules.append(module)
                    definition_string = element['definition']
                    definition = json.loads(definition_string)
                    variables = definition["variables"]
                    variable_list = []
                    var_dict = {}
                    for variable in variables:
                        name = variable["name"]
                        variable_type = variable["type"]
                        variable_list.append(name)
                        try:
                            readable_variable_type = self.types_dict[variable_type]
                            var_dict[name] = readable_variable_type
                        except KeyError:
                            print(f"Module {module} Variable {name} type {variable_type} not recognized!")
                    self.variables[module] = variable_list
                    self.types[module] = var_dict
                return True
            return False
        except requests.exceptions.ConnectionError:
            print("A Connection error occurred.")
            return False

    def variable_over_day(self, module_name, variable_names, start_date, end_date):
        """
        Gets variable in specific time range by connection with open database

        Args:
            module_name - name of module,
            variable_names - list of variable names,
            start_time - beginning of the time range
            stop_time - ending of the time range

        Returns:
            DataFrame: values for selected variable and time range

        """

        try:
            exist_vars = self.__check_if_exist(module_name, variable_names)
            if not exist_vars:
                return None
            variables_grouped = self.__check_variables(module_name, variable_names)
            response = self.__opendata.request_params(module_name=module_name,
                                                      grouped_variables=variables_grouped,
                                                      start_date=start_date,
                                                      end_date=end_date)
            return self.__opendata.parse_response(response)
        except requests.exceptions.ConnectionError:
            print("Error - Get data from OpenData")
            return None

    def __check_variables(self, module, variable):
        grouped_variables = list(map(lambda x: [x, self.types[module][x]], variable))
        tables = set(map(lambda x: x[1], grouped_variables))
        variables_grouped = [(x, [y[0] for y in grouped_variables if y[1] == x]) for x in tables]
        return variables_grouped

    def __check_if_exist(self, module: str, variables: list):
        """
        Verify if module or variable are in system

        Args:
            module
            variables

        Returns:
            True(bool) if exists
            raise ArgumentMissing error if not exists

        """

        if module not in self.types:
            print(f'Module: {module} not found')
            return False
        for variable in variables:
            if variable not in self.types[module]:
                print(f'Variable: {variable} not found')
                return False

        return True
