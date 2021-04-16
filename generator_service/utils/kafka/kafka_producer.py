import json
from dataclasses import dataclass
from typing import Any
from kafka import (
    KafkaProducer,
)
from .kafka_connector import (
    KafkaConfig,
)

class SimpleKafkaProducer:
    def __init__(self, config: KafkaConfig) -> None:
        self._kproducer =  KafkaProducer(bootstrap_servers=config.bootstrap_servers,
                             value_serializer=lambda v: json.dumps(v).encode('utf-8'))

        self._timeout = config.timeout

    def close(self) -> None:
        if self._kproducer != None:
            self._kproducer.close(self._timeout)
    
    def _on_send_success(self, record_metadata: Any):
        print("Send to topic: {}".format(record_metadata.topic))
        print("Send to partition: {}".format(record_metadata.partition))
        print("Send to offset: {}".format(record_metadata.offset))
        print("{}".format(record_metadata))
        
    def _on_send_error(self, excp):
        print("Error while publis message to Kafka", exc_info=excp)

    def send(self, topic: str, message: Any):
        self._kproducer.send(topic=topic, value=message) \
            .add_callback(self._on_send_success)\
            .add_errback(self._on_send_error)
        self._kproducer.flush(timeout=self._timeout)
