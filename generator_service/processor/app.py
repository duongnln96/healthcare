import csv
import json
import time

from utils import (
    KafkaConfig,
    SimpleKafkaProducer,
    SimpleKafkaConnector,
)

from .get_config import (
    AppConfig,
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
    def __init__(self, config: AppConfig) -> None:
        self._kafka_app = KafkaAppication(config.kafka_config)
        self._topic = config.topic_name
        self._data_path = config.data_path
        self._fieldnames = ('age', 'sex', 
                            'chest_pain_type', 'resting_blood_pressure', 
                            'cholesterol', 'fasting_blood_sugar', 'rest_ecg', 
                            'max_heart_rate_achieved', 'exercise_induced_angina', 
                            'st_depression', 'st_slope')
        self._csv_reader = None
        self._sampling_rate = config.sampling_rate

    def _create_topic(self, partition: int, relication: int):
        self._kafka_app.kafa_connector.create_topic(self._topic, partition, relication)

    def _send(self, message):
        self._kafka_app.kafka_producer.send(self._topic, message)

    def _read_data(self):
        csvfile = open(self._data_path, 'r')
        self._csv_reader = csv.DictReader(csvfile, self._fieldnames)

    def start(self):
        self._read_data()
        self._create_topic(partition=1, relication=1)
        for row in self._csv_reader:
            self._send(row)
            time.sleep(self._sampling_rate)
