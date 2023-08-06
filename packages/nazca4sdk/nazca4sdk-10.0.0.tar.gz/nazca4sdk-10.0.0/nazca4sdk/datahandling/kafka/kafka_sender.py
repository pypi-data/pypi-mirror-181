import json

from kafka import KafkaProducer, errors


class KafkaSender:

    def __init__(self):
        # self.__producer = KafkaProducer(bootstrap_servers='broker:10092')
        self.__producer = KafkaProducer(bootstrap_servers='10.217.1.201:10092')

    def send_message(self, topic: str, key: str, data: dict):
        try:
            d = json.dumps(data)
            self.__producer.send(topic=topic, key=bytes(key, 'utf-8'), value=str.encode(d))
            self.__producer.flush()
            return True
        except errors.KafkaError as e:
            print(e)
        return False
