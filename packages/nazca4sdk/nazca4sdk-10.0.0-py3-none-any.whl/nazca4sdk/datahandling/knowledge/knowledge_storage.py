from datetime import datetime

from nazca4sdk.datahandling.kafka.kafka_sender import KafkaSender
from nazca4sdk.datahandling.knowledge.knowledge_data_type import KnowledgeDataType
from nazca4sdk.datahandling.open_data_client import OpenDataClient


class KnowledgeStorage:

    def __init__(self, https=True):
        self.__openData = OpenDataClient(https)
        self.__kafkaSender = KafkaSender()

    def read_key_values(self, key: str):
        return self.__openData.read_knowledge_values(key)

    def write_key_values(self, key: str, section: str, value: str, datatype: KnowledgeDataType):
        if not KnowledgeDataType.has_value(datatype):
            print(f"KafkaDataType has no value  {datatype}")
            return None
        current_timestamp = datetime.now().isoformat()
        data_dict = {"timestamp": current_timestamp,
                     "key": key,
                     "property": section,
                     "value": value,
                     "dataType": datatype.value}
        return self.__kafkaSender.send_message("dataflow.fct.knowledge", key, data_dict)
