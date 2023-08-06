"""OpenData Client module"""
import datetime
import io
import json

import requests
from requests.exceptions import ConnectionError

from nazca4sdk.datahandling.cache.key_value import KeyValue
from nazca4sdk.datahandling.data_mod import Data
from nazca4sdk.datahandling.hotstorage.user_variable_value import UserVariableValue, UserVariablesValues
from nazca4sdk.datahandling.hotstorage.user_variables_info_value import UserVariablesInfoValues

JSON_HEADERS = {'Content-Type': 'application/json',
                'Accept': 'application/json'}


class DateTimeAwareEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.datetime):
            return o.isoformat()

        return json.JSONEncoder.default(self, o)


class OpenDataClient:
    """
    Get data from OpenData

    """

    def __init__(self, https: bool = True):
        """
        Initialize OpenData url to receive system configuration
        """

        if https:
            self.base_url = 'https://opendata:5001'
            self.base_url = 'https://10.217.1.201:10335'
        else:
            self.base_url = 'http://opendata:80'
            self.base_url = 'http://10.217.1.201:10335'

    @staticmethod
    def parse_response(response):
        """
        Parsing method

        """
        if response.status_code == 200:
            json_response = response.json()
            if 'message' in json_response:
                print("OpenData response failure")
                return None
            return Data(json_response)

        print("OpenData response error")
        return None

    def request_params(self, module_name, grouped_variables, **time):
        """
        Creates request for OpenData

        Args:
            module_name: module_name
            grouped_variables: list of variable names
            time: **time - Time definition:
                Possible pairs: start_date end_date or time_amount time_unit
        Returns:
            request for Open Data
        """
        headers = JSON_HEADERS
        try:
            if time.get("start_date") and time.get("end_date") is not None:
                request_params = [
                    ('module', module_name),
                    ('startdate', time['start_date']),
                    ('enddate', time['end_date'])
                ]

                for variable_type in grouped_variables:
                    for variable_name in variable_type[1]:
                        request_params.append((f'groupedVariables[{variable_type[0]}]',
                                               variable_name))

                response = requests.get(
                    f'{self.base_url}/api/HotStorage/VariableOverTime',
                    params=request_params,
                    headers=headers, verify=False)
                return response

        except AttributeError:
            print('Can not mix time descriptions, use start_date end_date'
                  ' or time amount with time unit')
            return None

    def save_variables(self, user_variables: [UserVariableValue]):
        if not isinstance(user_variables, list):
            raise ValueError("user variable is not a list")
        if not all(isinstance(x, UserVariableValue) for x in user_variables):
            raise ValueError("All object in user_variable list should by type UserVariable")
        headers = JSON_HEADERS
        try:
            variables = UserVariablesValues(__root__=user_variables)
            request_params = variables.json()
            response = requests.post(
                f'{self.base_url}/api/HotStorage/saveUserVariables',
                data=request_params,
                headers=headers, verify=False)
            return response

        except AttributeError:
            print('Can not mix time descriptions, use start_date end_date'
                  ' or time amount with time unit')
            return None

    def read_variables(self, user_variables_info: UserVariablesInfoValues):
        headers = JSON_HEADERS
        try:
            request_params = [
                ('startdate', user_variables_info.startDate),
                ('enddate', user_variables_info.endDate)
            ]

            for variable_type in user_variables_info.variables:
                for variable_name in user_variables_info.variables[variable_type]:
                    request_params.append((f'variables[{variable_type}]', variable_name))

            response = requests.get(
                f'{self.base_url}/api/HotStorage/userVariablesOverTime',
                params=request_params,
                headers=headers, verify=False)
            return response

        except AttributeError:
            print('Can not mix time descriptions, use start_date end_date'
                  ' or time amount with time unit')
            return None

    def download_file(self, path: str, local_path: str):
        """download file from file storage

        Args:
            path: path to file
            local_path: path to save the file

        Returns:
            binary of  file

        """
        headers = JSON_HEADERS
        try:
            request_params = [('path', path)]
            response = requests.get(
                f'{self.base_url}/api/FileRepository/file',
                params=request_params,
                headers=headers,
                verify=False)
        except ConnectionError:
            print(' Failed to establish connection to OpenData')
            return False
        except AttributeError:
            print(f'error while downloading file {path} from file repository')
            return False
        if response.status_code == 200:
            f = open(local_path, "wb")
            f.write(bytes(response.content))
            f.close()
            return True
        print(f"Error downloading file {path}, response.status_code={response.status_code}, "
              f"response.content={response.content}")
        return False

    def send_file(self, path: str, file: io.BytesIO):
        r"""send file to file storage

        Args:
            file: binary file to send
            path: path to file on file storage

        Returns:
            True - file saved, False - file save error

        """

        try:
            files = {'file': ("File.txt", file, "application/octet-stream")}
            request_params = [('path', path)]
            response = requests.post(
                f'{self.base_url}/api/FileRepository/file',
                params=request_params,
                files=files,
                verify=False)
        except ConnectionError as e:
            print(f'Failed to establish connection to OpenData {e}')
            return None
        except AttributeError:
            print(f'error while sending file {path} to file repository')
            return False
        if response.status_code == 200 or response.status_code == 204:
            print(f"file {path} saved.")
            return True
        print(f"Error sending file {path}, status code = {response.status_code}")
        return False

    def read_cache_keys(self, keys):
        headers = {'Accept': 'application/json'}
        try:

            request_params = {}
            for index in range(0, len(keys)):
                request_params[f"keys[{index}]"] = keys[index]

            response = requests.get(
                f'{self.base_url}/api/Cache',
                params=request_params,
                headers=headers,
                verify=False)
        except ConnectionError:
            print(' Failed to establish connection to OpenData')
            return None
        except AttributeError:
            print(f'error while get values for keys - {keys}')
            return None
        if response.status_code == 200:
            json_response = response.json()
            if 'message' in json_response:
                print("OpenData response failure")
                return None
            return json_response
        print(f"error while get values for keys - {keys}, response.status_code={response.status_code}, "
              f"response.content={response.content}")
        return None

    def write_cache_keys(self, key_values: KeyValue):
        """write key value to cache
        Args:
            key_values: dict key, value
        Returns:
              CacheEntry json if value saved or None if error
        """
        headers = JSON_HEADERS
        try:

            request_params = {"key": key_values.key,
                              "value": key_values.value}
            dump = json.dumps(request_params, cls=DateTimeAwareEncoder)
            response = requests.post(
                f'{self.base_url}/api/Cache/writeKeyValue',
                data=dump,
                headers=headers,
                verify=False)
        except ConnectionError:
            print(' Failed to establish connection to OpenData')
            return None
        except AttributeError:
            print(f'error while write values - {key_values}')
            return None
        if response.status_code == 200:
            json_response = response.json()
            if 'message' in json_response:
                print("OpenData response failure")
                return None
            return json_response
        print(f"error while write cache values - {key_values}, response.status_code={response.status_code}, "
              f"response.content={response.content}")
        return None

    def read_knowledge_values(self, key):
        headers = {'Accept': 'application/json'}
        try:

            request_params = {
                "key[eq]": key,
                "deepSearch": True,
                "count": 100,
                "offset": 0
            }

            response = requests.get(
                f'{self.base_url}/api/knowledge',
                params=request_params,
                headers=headers,
                verify=False)
        except ConnectionError:
            print(' Failed to establish connection to OpenData')
            return None
        except AttributeError:
            print(f'error while get knowledge for key - {key}')
            return None
        if response.status_code == 200:
            json_response = response.json()
            if 'message' in json_response:
                print("Get knowledge  failure")
                return None
            return json_response
        print(f"error while get knowledge for key - {key}, response.status_code={response.status_code}, "
              f"response.content={response.content}")
        return None

    def read_nazca_variables(self):
        headers = {'Accept': 'application/json'}
        response = requests.get(
            f'{self.base_url}/api/NazcaVariables', headers=headers, verify=False)
        return response

    def read_nazca_variable(self, identifier: str):
        headers = {'Accept': 'application/json'}
        response = requests.get(
            f'{self.base_url}/api/NazcaVariables/{identifier}', headers=headers, verify=False)
        return response
