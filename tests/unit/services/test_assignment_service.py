# Third-Party Library
import pytest
from dateutil import parser
from tests.data import DataStore

# Custom Library
from avionics_dash_server.services.assignment_service import AssignmentService


class TestAssignmentService:
    @pytest.fixture(scope="class")
    def setup_and_teardown_class(self):
        data_store = DataStore(collection_name="assignments")
        data_store.clean_up_collection()
        yield data_store
        data_store.clean_up_collection()

    @pytest.fixture(scope="function")
    def setup_and_teardown_func(self, setup_and_teardown_class):
        assignment_service = AssignmentService()
        yield assignment_service
        setup_and_teardown_class.clean_up_collection()

    def test_assignment_service_init(self):
        assignment_service = AssignmentService()
        assert isinstance(assignment_service, AssignmentService) is True

    def test_create_assignment(self, setup_and_teardown_func):
        assignment_service = setup_and_teardown_func
        assignment_obj = {
            "name": "Assignment-1",
            "desc": "Explain Principles of Flight with examples",
            "due": parser.parse("23/12/2022"),
            "points": "15",
            "submitted": False,
            "grade": "NA",
        }

        try:
            assignment_service.create_assignment(assignment_obj)
        except Exception as ex:
            assert False, f"Error while creating assignment. {ex}"
        assert True

    def test_by_name(self):
        pass

    @classmethod
    def create_assignment(cls, assignment_service):
        assignment_obj = {
            "name": "Assignment-1",
            "desc": "Explain Principles of Flight with examples",
            "due": parser.parse("23/12/2022"),
            "points": "15",
            "submitted": False,
            "grade": "NA",
        }

        try:
            assignment_service.create_assignment(assignment_obj)
        except Exception as ex:
            assert False, f"Error while creating assignment. {ex}"
        return assignment_obj
