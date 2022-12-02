# Third-Party Library
import pytest
from tests.data import DataStore

# Custom Library
from avionics_dash_server.app import create_app


class TestApi:
    @pytest.fixture(scope="class")
    def setup_and_teardown_class(self):
        data_store = DataStore(collection_name="users")
        yield data_store
        data_store.clean_up_user_collection()

    @pytest.fixture(scope="function")
    def setup_and_teardown_func(self, setup_and_teardown_class):
        app = create_app()
        with app.test_client() as test_client:
            yield test_client
        setup_and_teardown_class.clean_up_user_collection()

    def test_api_root(self, setup_and_teardown_func):
        test_client = setup_and_teardown_func
        response = test_client.get("/api/v1/")
        assert response.status_code == 200
        assert response.json == {"message": "Hello from Avionics Dash API!"}

    def test_api_status(self, setup_and_teardown_func):
        test_client = setup_and_teardown_func
        response = test_client.get("/api/v1/status")
        assert response.status_code == 200
        assert response.json == {"message": "Avionics Dash API running...OK"}

    def test_register(self, setup_and_teardown_func):
        test_client = setup_and_teardown_func

        user_data = {
            "first_name": "Mike",
            "last_name": "Ross",
            "email": "abcd@abc.com",
            "password": "abcd1234",
        }
        response = test_client.post(
            "/api/v1/auth/register", json={"data": user_data}, headers={"Content-Type": "application/json"}
        )

        assert response.status_code == 201
        assert response.json == {}

    def test_login(self, setup_and_teardown_func):
        test_client = setup_and_teardown_func
        self.create_user(test_client)
        response = test_client.post(
            "/api/v1/auth/login",
            json={"email": "abcd@abc.com", "password": "abcd1234"},
            headers={"Content-Type": "application/json"},
        )
        assert response.status_code == 201
        assert "token" in response.json

    @classmethod
    def create_user(cls, test_client):
        user_data = {
            "first_name": "Mike",
            "last_name": "Ross",
            "email": "abcd@abc.com",
            "password": "abcd1234",
        }
        response = test_client.post(
            "/api/v1/auth/register", json={"data": user_data}, headers={"Content-Type": "application/json"}
        )

        assert response.status_code == 201
        assert response.json == {}
