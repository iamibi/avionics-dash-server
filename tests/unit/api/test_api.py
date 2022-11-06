# Third-Party Library
import pytest

# Custom Library
from avionics_dash_server.app import create_app


class TestApi:
    @pytest.fixture(scope="class")
    def setup(self):
        app = create_app()
        with app.test_client() as test_client:
            yield test_client

    def test_api_root(self, setup):
        test_client = setup
        response = test_client.get("/api/")
        assert response.status_code == 200
        assert response.json == {"message": "Hello from Avionics Dash API!"}

    def test_api_status(self, setup):
        test_client = setup
        response = test_client.get("/api/v1/status")
        assert response.status_code == 200
        assert response.json == {"message": "Avionics Dash API running...OK"}
