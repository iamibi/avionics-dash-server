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
        response = test_client.get("/api/v1/")
        assert response.status_code == 200
        assert response.json == {"message": "Hello from Avionics Dash API!"}

    def test_api_status(self, setup):
        test_client = setup
        response = test_client.get("/api/v1/status")
        assert response.status_code == 200
        assert response.json == {"message": "Avionics Dash API running...OK"}

    def test_login(self, setup):
        test_client = setup
        response = test_client.post(
            "/api/v1/auth/login", json={"username": "test"}, headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 201
        assert "token" in response.json

    def test_verify(self, setup):
        test_client = setup
        response = test_client.post(
            "/api/v1/auth/login", json={"username": "test"}, headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 201

        token = response.json["token"]
        response = test_client.get("/api/v1/auth/verify", headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 200
        assert response.json["message"] == "The token is valid!"
