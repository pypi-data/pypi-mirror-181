from nazca4sdk.datahandling.hotstorage.helper import transform_info, transform, create_variables_frame
from nazca4sdk.datahandling.hotstorage.model.user_variable import UserVariable, \
    UserVariableInfo
from nazca4sdk.datahandling.hotstorage.user_variable_value import UserVariablesValues
from nazca4sdk.datahandling.hotstorage.user_variables_info_value import UserVariablesInfoValues, UserVariableInfoValue
from nazca4sdk.datahandling.kafka.kafka_sender import KafkaSender
from nazca4sdk.datahandling.open_data_client import OpenDataClient


class HotStorage:
    def __init__(self, https=True):
        self.__openData = OpenDataClient(https)
        self.__kafkaSender = KafkaSender()

    def save_variables(self, user_variables: [UserVariable]):

        variables = transform(user_variables)
        if len(variables) == 0:
            return False
        user_variables_frame = create_variables_frame(variables)
        return self.__kafkaSender.send_message("dataflow.fct.clickhouse", 'Variables', user_variables_frame)

    def read_variables(self, start_date: str, end_date: str, variables: [UserVariableInfo]):
        variables = transform_info(variables)
        if not isinstance(variables, list):
            raise ValueError("variables is not a list")
        if not variables:
            raise ValueError("variables is empty")
        if not all(isinstance(x, UserVariableInfoValue) for x in variables):
            raise ValueError("All object in user_variable list should by type UserVariable")
        user_variables = UserVariablesInfoValues(startDate=start_date, endDate=end_date)
        [user_variables.add_variable(variable) for variable in variables]
        variables_response = self.__openData.read_variables(user_variables)
        if variables_response.status_code == 200:
            variables_list = UserVariablesValues.parse_raw(variables_response.content)
            return variables_list.variables()
        else:
            print("error reading user variables")
            return []
