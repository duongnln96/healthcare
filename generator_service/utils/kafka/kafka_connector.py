import logging
from dataclasses import dataclass
from kafka.admin import (
    KafkaAdminClient, 
    NewTopic,
)

@dataclass
class KafkaConfig(object):
    bootstrap_servers: str
    timeout: int

class SimpleKafkaConnector:
    def __init__(self, config: KafkaConfig) -> None:
        self._connector = KafkaAdminClient(bootstrap_servers=config.bootstrap_servers)
        self._timeout = config.timeout

    def close(self) -> None:
        if self._connector != None:
            self._connector.close()

    def create_topic(self, topic: str, partitions: int, relicas: int) -> None:
        """Create new topics in the cluster."""        
        try:
            topic_list = []
            topic_list.append(NewTopic(topic, partitions, relicas))
            self._connector.create_topics(new_topics=topic_list, timeout_ms=self._timeout)
            logging.warning("Create new topics: {} in the cluster".format(topic))
        except Exception as ex:
            logging.exception("Error while creating the kafka topic: {}".format(ex))
