# Standard Library
import os
from string import Template
from typing import Dict, Union, NamedTuple
from collections import namedtuple

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
    DATABASE_CONFIG = os.path.join(SETTINGS_PATH, "mongo.yml")
    CREDENTIALS = os.path.join(SETTINGS_PATH, "credentials.yml")

    __config: NamedTuple = None

    def __init__(self) -> None:
        env = self.__get_env(const.App.APP_ENV)

        if env not in const.App.VALID_ENVS:
            raise exs.ConfigurationError("Invalid environment value!")

        try:
            self.__read_configurations(env)
        except exs.ConfigurationError:
            raise
        except Exception:
            raise exs.ConfigurationError("Something went wrong!")

    @property
    def config(self):
        return self.__config

    def __read_configurations(self, env: str) -> None:
        configurations = self.__get_env_config_values(env)
        self.__config = self.__dict_to_namedtuple("config", configurations)

    def __get_env_config_values(self, env: str) -> Dict:
        app_config = self._read_file(self.SETTINGS_CONFIG)
        db_config = self._read_file(self.DATABASE_CONFIG)
        credentials = self._read_file(self.CREDENTIALS)

        configurations = app_config[env]

        if "db" in configurations or "credentials" in configurations:
            raise exs.ConfigurationError("Config Key Error!")

        configurations["db"] = db_config[env]
        configurations["credentials"] = self.__get_env_credentials(env=env, credentials=credentials)

        return configurations

    def __get_env_credentials(self, env: str, credentials: Dict) -> Dict:
        env_credentials = credentials[env]
        if env == const.App.TEST_ENV:
            return env_credentials

        # self.__set_db_credentials(env_credentials["db"])
        self.__set_jwt_credentials(env_credentials["jwt"])
        return env_credentials

    def __set_db_credentials(self, credentials: Dict) -> None:
        username = credentials[const.Credentials.USERNAME]
        password = credentials[const.Credentials.PASSWORD]

        env_username = self.__get_env(key=const.App.Env.DB_USERNAME)
        env_password = self.__get_env(key=const.App.Env.DB_PASSWORD)

        if env_username in {None, ""} or env_password in {None, ""}:
            raise exs.ConfigurationError("Unable to fetch database username/password!")

        credentials[const.Credentials.USERNAME] = Template(username).substitute(
            {const.Credentials.DB[const.Credentials.USERNAME]: env_username}
        )

        credentials[const.Credentials.PASSWORD] = Template(password).substitute(
            {const.Credentials.DB[const.Credentials.PASSWORD]: env_password}
        )

    def __set_jwt_credentials(self, credentials: Dict) -> None:
        key_name = credentials[const.Credentials.KEY]
        env_key_val = self.__get_env(key=const.App.Env.JWT_KEY)

        if env_key_val in {None, ""}:
            raise exs.ConfigurationError("Unable to fetch JWT key!")

        credentials[const.Credentials.KEY] = Template(key_name).substitute(
            {const.Credentials.JWT[const.Credentials.KEY]: env_key_val}
        )

    @classmethod
    def __get_env(cls, key: str) -> Union[str, None]:
        return os.getenv(key=key)

    def __dict_to_namedtuple(self, typename: str, data: Dict) -> NamedTuple:
        return namedtuple(typename, data.keys())(
            *(self.__dict_to_namedtuple(typename + "_" + k, v) if isinstance(v, dict) else v for k, v in data.items())
        )


# Create a singleton to be called by all the other modules
settings = _Settings().config
