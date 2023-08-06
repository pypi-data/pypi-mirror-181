import json
from kafka import KafkaProducer, KafkaConsumer
import traceback
import sys
from json import dumps, loads
import dataclasses 
from enum import Enum

# Main class
class BrokerStreams():

    def __init__(self, consume_topic_name, producer_topic_name, broker_url):
        self.___producer = None
        self.___consumer = None
        self.___consume_topic_name = consume_topic_name
        self.___producer_topic_name = producer_topic_name
        self.___broker_url = broker_url
        self.__initiliaze()

    def __initiliaze(self):
        try:
            self.___consumer = KafkaConsumer(
                self.___consume_topic_name,
                bootstrap_servers=[self.___broker_url],
                auto_offset_reset='earliest',
                enable_auto_commit=True,
                value_deserializer=lambda x: loads(x.decode('utf-8'))
            )
            self.___producer = KafkaProducer(
                bootstrap_servers=[self.___broker_url],
                value_serializer=lambda x: dumps(x).encode('utf-8'),
                api_version=(0, 10, 1),
            )
        except Exception as e:
            print(traceback.format_exc())
            print(sys.exc_info()[2])
            raise traceback.format_exc()


    def send_message(self, data, topic_name=None):
        try:
            if not None:
                self.___producer.send(topic_name, data)
            else:
                self.___producer.send(self.___producer_topic_name, data)
        except Exception as e:
            print(traceback.format_exc())
            print(sys.exc_info()[2])
            raise traceback.format_exc()

    def consume_topic(self):
        try:
            return self.___consumer
        except Exception as e:
            print(traceback.format_exc())
            print(sys.exc_info()[2])
            raise traceback.format_exc()

    def consume_topics(self, subscribes):
        """Consume all topics with a given subscription"""
        try:
            self.consume_topic().subscribe(subscribes)
        except Exception as e:
            print(traceback.format_exc())
            print(sys.exc_info()[2])
            raise traceback.format_exc()


class Connectors(Enum):
    INSTA = 'INSTA'
    LINKEDIN = 'LINKEDIN'
    FACEBOOK = 'FACEBOOK'

class StatusSearch(Enum):
    RUNNING = 'RUNNING'
    FAILED = 'FAILED'
    SUCCESS = 'SUCCESS'

class SearchType(Enum):
    FLN = 'FIRST_LAST_NAME'
    EMAIL = 'EMAIL'
    LINK = 'LINK'

@dataclasses.dataclass
class DtoBk:
    user_id: str
    search_id: str
    search_type: list  
    connectors: list
    status: StatusSearch
    data: dict

    def get_dict(self):
        return dataclasses.asdict(self)
