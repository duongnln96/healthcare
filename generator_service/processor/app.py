import time
import logging

from utils import (
    KafkaConfig,
    SimpleKafkaProducer,
    SimpleKafkaConnector,
)

from .get_config import (
    AppConfig,
)

from .heart_disease_model import (
    HeartDiseaseModel,
    HeartDiseaseDataGenerator,
)

class KafkaAppication:
    def __init__(self, config: KafkaConfig) -> None:
        self._kafa_connector = SimpleKafkaConnector(config)
        self._kafka_producer = SimpleKafkaProducer(config)

    @property
    def kafa_connector(self): 
        return self._kafa_connector

    @property
    def kafka_producer(self): 
        return self._kafka_producer


class Application:

    DEFAULT_NUM_INTERATION = 500
    DEFAULT_NUM_RECORD = 1000

    def __init__(self, config: AppConfig) -> None:
        self._kafka_app = KafkaAppication(config.kafka_config)
        self._topic = config.topic_name
        self._sampling_rate = config.sampling_rate

    def _send(self, message):
        self._kafka_app.kafka_producer.send(self._topic, message)

    def _generate_heart_disease(self, num_record=DEFAULT_NUM_RECORD, num_iter=DEFAULT_NUM_INTERATION):
        for _ in range(num_iter):
            data = HeartDiseaseDataGenerator().generate(num_record)
            start = time.time()
            for elem in data:
                self._send(elem)
            end = time.time()
            logging.warning("Send {} into {}s".format(num_record, end - start))
            time.sleep(self._sampling_rate)

    @classmethod
    def start(cls, config: AppConfig):
        obj = cls(config=config)
        obj._generate_heart_disease()
