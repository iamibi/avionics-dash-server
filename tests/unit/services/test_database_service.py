# Third-Party Library
from tests.data import DataStore
import pytest

# Custom Library
from avionics_dash_server.services.database_service import DatabaseService


class TestDatabaseService(DataStore):
    @pytest.fixture(scope="class")
    def setup_and_teardown(self):
        database_service = DatabaseService()
        yield database_service
        del database_service

    def test_database_init(self):
        try:
            DatabaseService()
        except Exception as exc:
            assert False, f"DatabaseService init failed with error: {exc}"

    def test_create_index_valid(self):
        pass

    def test_create_index_invalid(self):
        pass
