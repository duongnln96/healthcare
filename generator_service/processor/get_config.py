import os
from envyaml import EnvYAML
from dataclasses import dataclass

from utils import (
    KafkaConfig,
)

@dataclass
class AppConfig:
    kafka_config: KafkaConfig
    topic_in: str
    topic_out: str
    sampling_rate: int

class GetAppConfig(object):
    def __init__(self):
        self.__config_path = "./config_local.yaml"
        self.__config: EnvYAML = EnvYAML(self.__config_path)

    def _get_kafka_configs(self) -> KafkaConfig:
        bootstrap_servers: str = self.__config["kafka_management"]["bootstrap_servers"]
        timeout: int = self.__config["kafka_management"]["timeout"]

        return KafkaConfig(bootstrap_servers, timeout)

    def _get_topic_in(self) -> str:
        return self.__config["kafka_management"]["topic_in"]

    def _get_topic_out(self) -> str:
        return self.__config["kafka_management"]["topic_out"]

    def _get_samling_rate(self) -> int:
        return self.__config["sampling_rate"]

    def get_app_config(self) -> AppConfig:
        kafka_config: KafkaConfig = self._get_kafka_configs()
        topic_in: str = self._get_topic_in()
        topic_out: str = self._get_topic_out()
        sampling_rate: int = self._get_samling_rate()

        return AppConfig(kafka_config, topic_in, 
                        topic_out, sampling_rate)
