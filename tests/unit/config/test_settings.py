# Standard Library
from typing import NamedTuple

# Third-Party Library
import pytest


class TestSettings:
    @pytest.fixture(scope="class")
    def setup(self):
        # Custom Library
        from avionics_dash_server.config.settings import settings
        yield settings

    def test_settings_import(self):
        try:
            # Custom Library
            from avionics_dash_server.config.settings import settings
        except ImportError:
            assert False, "Unable to create settings object"

    def test_settings_value(self, setup):
        settings = setup
        assert settings is not None
        assert settings.placeholder == "placeholder"

    def test_database_config_value(self, setup):
        settings = setup

        assert settings.db is not None
        assert settings.db.avionics_dash is not None
        assert settings.db.avionics_dash.db_name == "avionics_dash_test"

    def test_credentials_value(self, setup):
        settings = setup

        assert settings.credentials is not None
        assert settings.credentials.db is not None
        assert settings.credentials.db.username == "testUser"
        assert settings.credentials.db.password == "testPassword"
