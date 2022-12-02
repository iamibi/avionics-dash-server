# Third-Party Library
import pytest
from tests.data import DataStore

# Custom Library
from avionics_dash_server.services.user_service import UserService


class TestUserService:
    @pytest.fixture(scope="class")
    def setup_and_teardown_class(self):
        data_store = DataStore(collection_name="users")
        yield data_store
        data_store.clean_up_user_collection()

    @pytest.fixture(scope="function")
    def setup_and_teardown_func(self, setup_and_teardown_class):
        user_service = UserService()
        yield user_service
        setup_and_teardown_class.clean_up_user_collection()

    def test_user_service_init(self):
        user_service = UserService()
        assert user_service is not None

    def test_create_user(self, setup_and_teardown_func):
        user_service = setup_and_teardown_func

        user_obj = {"email": "abc@abc.com", "password": "abcd1234", "first_name": "Mike", "last_name": "Ross"}
        try:
            user_service.create_user(user_obj)
            assert True
        except Exception as ex:
            assert False, f"Failed to create user. Error: {ex}"

    def test_by_email(self, setup_and_teardown_func):
        user_service = setup_and_teardown_func

        user_obj = self.create_test_user(user_service)

        try:
            user = user_service.by_email(email_id="abc@abc.com")
        except Exception as ex:
            assert False, f"Failed to fetch user. Error: {ex}"

        all_keys = ("_id", "email", "first_name", "last_name", "created_at", "updated_at")
        assert sorted(tuple(user.keys())) == sorted(all_keys)
        assert user["email"] == user_obj["email"]

    def test_by_email_with_password(self, setup_and_teardown_func):
        user_service = setup_and_teardown_func

        user_obj = self.create_test_user(user_service)

        try:
            user = user_service.by_email(email_id="abc@abc.com", with_pass=True)
        except Exception as ex:
            assert False, f"Failed to fetch user. Error: {ex}"

        all_keys = ("_id", "email", "password", "first_name", "last_name", "created_at", "updated_at")
        assert sorted(tuple(user.keys())) == sorted(all_keys)
        assert user["email"] == user_obj["email"]
        assert isinstance(user["password"], dict) is True

        password_keys = ("password_hash", "updated_at", "created_at")
        assert sorted(tuple(user["password"].keys())) == sorted(password_keys)
        assert isinstance(user["password"]["password_hash"], str) is True

    @classmethod
    def create_test_user(cls, user_service):
        user_obj = {"email": "abc@abc.com", "password": "abcd1234", "first_name": "Mike", "last_name": "Ross"}
        try:
            user_service.create_user(user_obj)
        except Exception as ex:
            assert False, f"Failed to create user. Error: {ex}"
        return user_obj