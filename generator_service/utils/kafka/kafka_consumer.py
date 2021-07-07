import json
import logging
from typing import Any
from kafka import (
    KafkaConsumer
)
from .kafka_connector import (
    KafkaConfig,
)

class SimpleKafkaConsumer:
    def __init__(self, config: KafkaConfig) -> None:
        self._kconsumer =  KafkaConsumer(bootstrap_servers=config.bootstrap_servers,
                            client_id="HeartDisease-Consumer",
                            value_deserializer=lambda v: json.loads(v.decode('utf-8')),
                            auto_offset_reset='latest')

        self._timeout = config.timeout

    def consume_topic(self, topic: str):
        self._kconsumer.subscribe([topic])

        return self._kconsumer

    def stop_consume(self):
        self._kconsumer.close()
