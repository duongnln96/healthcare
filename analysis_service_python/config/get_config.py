import os
from envyaml import EnvYAML
from dataclasses import dataclass

from utils import (
    KafkaConfig,
)

@dataclass
class AppConfig:
    kafka_config: KafkaConfig
    topic_result: str
    topic_raw: str
    model_path: str

class GetAppConfig(object):
    def __init__(self):
        self.__config_path = "./config/config_local.yaml"
        if self.__config_path is None:
            raise Exception("The config path is not correct")
        self.__config: EnvYAML = EnvYAML(self.__config_path)

    def _get_kafka_configs(self) -> KafkaConfig:
        bootstrap_servers: str = self.__config["kafka_management"]["bootstrap_servers"]
        timeout: int = self.__config["kafka_management"]["timeout"]

        return KafkaConfig(bootstrap_servers, timeout)

    def _get_topic_raw(self) -> str:
        return self.__config["kafka_management"]["topic_raw"]

    def _get_topic_result(self) -> str:
        return self.__config["kafka_management"]["topic_result"]

    def _get_model_path(self) -> str:
        return self.__config["model_path"]

    def get_app_config(self) -> AppConfig:
        kafka_config: KafkaConfig = self._get_kafka_configs()
        topic_result: str = self._get_topic_result()
        topic_raw: str = self._get_topic_raw()
        model_path: str = self._get_model_path()

        return AppConfig(
            kafka_config=kafka_config, 
            topic_result=topic_result,
            topic_raw=topic_raw,
            model_path=model_path)
