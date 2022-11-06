class TestSettings:
    def test_settings(self):
        try:
            # Custom Library
            from avionics_dash_server.config.settings import settings
        except ImportError:
            assert False, "Unable to create settings object"
        assert settings is not None
        assert settings.placeholder == "placeholder"
