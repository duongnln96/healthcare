import os
from envyaml import EnvYAML
from dataclasses import dataclass

from utils import (
    KafkaConfig,
)

@dataclass
class AppConfig:
    kafka_config: KafkaConfig
    topic_name: str
    data_path: str
    sampling_rate: int

class GetAppConfig(object):
    def __init__(self, args):
        self.__args = args
        if self.__args.local:
            self.__config_path = "./config_local.yaml"
        else:
            self.__config_path = os.getenv("CONF_FILE")
        if self.__config_path is None:
            raise Exception("The config path is not correct")
        self.__config: EnvYAML = EnvYAML(self.__config_path)

    def _get_kafka_configs(self) -> KafkaConfig:
        bootstrap_servers: str = self.__config["kafka_management"]["bootstrap_servers"]
        timeout: int = self.__config["kafka_management"]["timeout"]

        return KafkaConfig(bootstrap_servers, timeout)

    def _get_topic(self) -> str:
        return self.__config["kafka_management"]["topic"]

    def _get_data_path(self) -> str:
        return self.__config["data_path"]

    def _get_samling_rate(self) -> int:
        return self.__config["sampling_rate"]

    def get_app_config(self) -> AppConfig:
        kafka_config: KafkaConfig = self._get_kafka_configs()
        topic_name: str = self._get_topic()
        data_path: str = self._get_data_path()
        sampling_rate: int = self._get_samling_rate()

        return AppConfig(kafka_config, topic_name, 
                        data_path, sampling_rate)
