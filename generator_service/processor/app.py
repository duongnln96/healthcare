import time
import pandas as pd
from pandas.io.pytables import SeriesFixed

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
        self._data_path = config.data_path
        self._fieldnames = ('age', 'sex', 
                            'chest_pain_type', 'resting_blood_pressure', 
                            'cholesterol', 'fasting_blood_sugar', 'rest_ecg', 
                            'max_heart_rate_achieved', 'exercise_induced_angina', 
                            'st_depression', 'st_slope')
        self._data_table = None
        self._sampling_rate = config.sampling_rate

    def _create_topic(self, partition: int, relication: int):
        self._kafka_app.kafa_connector.create_topic(self._topic, partition, relication)

    def _send(self, message):
        self._kafka_app.kafka_producer.send(self._topic, message)

    def _read_data_pandas(self):
        df = pd.read_csv(self._data_path, usecols=self._fieldnames)
        self._data_table = df.to_dict(orient='records')

    def _generate_heart_disease(self, num_record=DEFAULT_NUM_RECORD, num_iter=DEFAULT_NUM_INTERATION):
        for _ in range(num_iter):
            data = HeartDiseaseDataGenerator().generate(num_record)
            for elem in data:
                self._send(elem)
            time.sleep(self._sampling_rate)

    def start(self):
        self._create_topic(partition=1, relication=1)
        self._generate_heart_disease()
