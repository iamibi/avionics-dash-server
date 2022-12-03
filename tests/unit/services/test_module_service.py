# Standard Library
from datetime import datetime

# Third-Party Library
import pytest
from bson import ObjectId
from tests.data import DataStore

# Custom Library
from avionics_dash_server.models.course_model import Module
from avionics_dash_server.services.module_service import ModuleService


class TestModuleService:
    @pytest.fixture(scope="class")
    def setup_and_teardown_class(self):
        data_store = DataStore(collection_name="modules")
        data_store.clean_up_collection()
        yield data_store
        data_store.clean_up_collection()

    @pytest.fixture(scope="function")
    def setup_and_teardown_func(self, setup_and_teardown_class):
        module_service = ModuleService()
        yield module_service
        setup_and_teardown_class.clean_up_collection()

    def test_module_service_init(self):
        module_service = ModuleService()
        assert isinstance(module_service, ModuleService) is True

    def test_create_module(self, setup_and_teardown_func):
        module_service = setup_and_teardown_func

        module_obj = {
            "name": "Becoming a Private Pilot",
            "desc": "What does it take to become a Private Pilot? You will know right after this module",
            "url": "https://www.youtube.com/watch?v=WZOk2Y65_5w&t=3s",
        }

        try:
            module_service.create_module(module_obj)
        except Exception as ex:
            assert False, f"Error while creating module. {ex}"
        assert True

    def test_by_name(self, setup_and_teardown_func):
        module_service = setup_and_teardown_func
        self.create_module(module_service)

        try:
            module = module_service.by_name(module_name="Becoming a Private Pilot")
        except Exception as ex:
            assert False, f"Error while fetching by name. {ex}"
        assert isinstance(module, Module) is True
        assert isinstance(module.identifier, ObjectId) is True
        assert module.name == "Becoming a Private Pilot"
        assert module.desc == "What does it take to become a Private Pilot? You will know right after this module"
        assert module.url == "https://www.youtube.com/watch?v=WZOk2Y65_5w&t=3s"
        assert isinstance(module.created_at, datetime) is True
        assert isinstance(module.updated_at, datetime) is True
        assert module.created_at.tzname() == "UTC"
        assert module.updated_at.tzname() == "UTC"

    def test_by_id(self, setup_and_teardown_func):
        module_service = setup_and_teardown_func
        self.create_module(module_service)

        try:
            module_by_name = module_service.by_name(module_name="Becoming a Private Pilot")
            module = module_service.by_id(module_id=module_by_name.identifier)
        except Exception as ex:
            assert False, f"Error while fetching by id. {ex}"
        assert isinstance(module, Module) is True
        assert isinstance(module.identifier, ObjectId) is True
        assert module_by_name.identifier == module.identifier
        assert module.name == "Becoming a Private Pilot"
        assert module.desc == "What does it take to become a Private Pilot? You will know right after this module"
        assert module.url == "https://www.youtube.com/watch?v=WZOk2Y65_5w&t=3s"
        assert isinstance(module.created_at, datetime) is True
        assert isinstance(module.updated_at, datetime) is True
        assert module.created_at.tzname() == "UTC"
        assert module.updated_at.tzname() == "UTC"

    @classmethod
    def create_module(cls, module_service):
        module_obj = {
            "name": "Becoming a Private Pilot",
            "desc": "What does it take to become a Private Pilot? You will know right after this module",
            "url": "https://www.youtube.com/watch?v=WZOk2Y65_5w&t=3s",
        }

        try:
            module_service.create_module(module_obj)
        except Exception as ex:
            assert False, f"Error while creating module. {ex}"
        return module_obj
