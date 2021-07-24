import time
import statistics
from datetime import datetime

from utils import (
    KafkaConfig,
    SimpleKafkaProducer,
    SimpleKafkaConnector,
    SimpleKafkaConsumer,
    logging,
)

from .get_config import (
    AppConfig,
)

from .heart_disease_model import (
    HeartDiseaseDataGenerator,
)

DEFAULT_NUM_INTERATION = 100
DEFAULT_NUM_RECORD = 1000

class KafkaAppication:
    def __init__(self, config: KafkaConfig) -> None:
        self._kafa_connector = SimpleKafkaConnector(config)
        self._kafka_producer = SimpleKafkaProducer(config)
        self._kafka_consumer = SimpleKafkaConsumer(config)

    @property
    def kafa_connector(self):
        return self._kafa_connector

    @property
    def kafka_producer(self):
        return self._kafka_producer

    @property
    def kafka_consumer(self):
        return self._kafka_consumer


class ProduceApplication:
    CLASS_NAME = __name__

    def __init__(self, config: AppConfig) -> None:
        self._kproducer = KafkaAppication(config.kafka_config).kafka_producer
        self._topic = config.topic_in
        self._sampling_rate = config.sampling_rate
        self._log = logging.get_logger(self.CLASS_NAME)

    def _send(self, message):
        self._kproducer.send(self._topic, message)

    def _generate_heart_disease(self, num_record=DEFAULT_NUM_RECORD, num_iter=DEFAULT_NUM_INTERATION):
        for _ in range(num_iter):
            data = HeartDiseaseDataGenerator().generate(num_record)
            start = time.time()
            for elem in data:
                self._send(elem)
            end = time.time()
            logging.info(self._log, "Send {} into {}s".format(num_record, end - start))
            time.sleep(self._sampling_rate)

    @classmethod
    def start(cls, config: AppConfig):
        obj = cls(config=config)
        obj._generate_heart_disease()


class ComsumeApplication:
    CLASS_NAME = __name__
    def __init__(self, config: AppConfig) -> None:
        self._kcomsumer = KafkaAppication(config.kafka_config).kafka_consumer
        self._topic = config.topic_out
        self._log = logging.get_logger(self.CLASS_NAME)
        self._latencies = []

    def _consume_messages(self):
        try:
            messages = self._kcomsumer.consume_topic(self._topic)
            for msg in messages:
                if msg is None:
                    continue
                else:
                    latency = (datetime.now().timestamp()*1000) - msg.timestamp
                    self._latencies.append(latency)
        except KeyboardInterrupt:
            self._consume_stop()
            self._report()

    def _report(self):
        if len(self._latencies) != 0:
            logging.info(self._log, "{} messages consumed".format(len(self._latencies)))
            logging.info(self._log, "mean latency: {}ms".format(statistics.mean(self._latencies)))
            logging.info(self._log, "max latency: {}ms".format(max(self._latencies)))
        else:
            logging.err(self._log, "Cannot get any messages")

    def _consume_stop(self):
        self._kcomsumer.stop_consume()

    @classmethod
    def start(cls, config: AppConfig):
        obj = cls(config=config)
        obj._consume_messages()
