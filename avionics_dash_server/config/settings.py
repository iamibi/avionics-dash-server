# Standard Library
from typing import Dict, Union, NamedTuple
from collections import namedtuple
import os

# Third-Party Library
import yaml

# Custom Library
from avionics_dash_server.common import constants as const
from avionics_dash_server.common import exceptions as exs


class _ConfigParser:
    @classmethod
    def _read_file(cls, filename: str) -> Dict:
        mode = "r"
        encoding = "utf-8"
        try:
            with open(file=filename, mode=mode, encoding=encoding) as data:
                return yaml.safe_load(data)
        except yaml.YAMLError as exc:
            raise exs.ConfigurationError("Unable to read the configuration file!")


class _Settings(_ConfigParser):
    """Base settings class that is protected and should be used within this file only"""

    SETTINGS_PATH = os.path.dirname(os.path.abspath(__file__))
    SETTINGS_CONFIG = os.path.join(SETTINGS_PATH, "settings.yml")

    __config: NamedTuple = None

    def __init__(self) -> None:
        env = self.__get_env(const.App.APP_ENV)

        if env not in const.App.VALID_ENVS:
            raise exs.ConfigurationError("Invalid environment value!")

        self.__read_configurations(env)

    @property
    def config(self):
        return self.__config

    def __read_configurations(self, env: str) -> None:
        configurations = self.__get_env_config_values(env)
        self.__config = self.__dict_to_namedtuple("config", configurations)

    def __get_env_config_values(self, env: str) -> Dict:
        app_config = self._read_file(self.SETTINGS_CONFIG)
        configurations = app_config[env]

        return configurations

    @classmethod
    def __get_env(cls, key: str) -> Union[str, None]:
        return os.getenv(key=key)

    def __dict_to_namedtuple(self, typename: str, data: Dict) -> NamedTuple:
        return namedtuple(typename, data.keys())(
            *(self.__dict_to_namedtuple(typename + "_" + k, v) if isinstance(v, dict) else v for k, v in data.items())
        )


# Create a singleton to be called by all the other modules
settings = _Settings().config
