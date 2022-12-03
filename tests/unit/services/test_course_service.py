# Third-Party Library
import pytest
from dateutil import parser
from tests.data import DataStore

# Custom Library
from avionics_dash_server.services.course_service import CourseService
from avionics_dash_server.services.module_service import ModuleService
from avionics_dash_server.services.assignment_service import AssignmentService


class TestCourseService:
    @pytest.fixture(scope="class")
    def setup_and_teardown_class(self):
        data_store_course = DataStore(collection_name="courses")
        data_store_modules = DataStore(collection_name="modules")
        data_store_assignments = DataStore(collection_name="assignments")

        data_store_course.clean_up_collection()
        data_store_modules.clean_up_collection()
        data_store_assignments.clean_up_collection()

        yield data_store_course, data_store_modules, data_store_assignments

        data_store_course.clean_up_collection()
        data_store_modules.clean_up_collection()
        data_store_assignments.clean_up_collection()

    @pytest.fixture(scope="function")
    def setup_and_teardown_func(self, setup_and_teardown_class):
        course_service = CourseService()
        module_service = ModuleService()
        assignment_service = AssignmentService()

        yield course_service, module_service, assignment_service

        data_store_course, data_store_modules, data_store_assignments = setup_and_teardown_class
        data_store_course.clean_up_collection()
        data_store_modules.clean_up_collection()
        data_store_assignments.clean_up_collection()

    def test_course_service_init(self):
        course_service = CourseService()
        assert isinstance(course_service, CourseService) is True

    def test_create_course(self, setup_and_teardown_func):
        course_service, module_service, assignment_service = setup_and_teardown_func

        module_obj = self.create_module(module_service)
        assignment_obj = self.create_assignment(assignment_service)
        module = module_service.by_name(module_name=module_obj["name"])
        assignment = assignment_service.by_name(assignment_name=assignment_obj["name"])

        course_obj = {
            "img": "/courses/c1.jpeg",
            "title": "Private Pilot Made Easy Online Ground School",
            "price": "- $890",
            "desc": "Our online ground school will help you pass the FAA Private Pilot test with flying colors. "
            "Achieve your dreams of flying an airplane.",
            "modules": [module.identifier],
            "assignments": [assignment.identifier],
        }

        try:
            course_service.create_course(course=course_obj)
        except Exception as ex:
            assert False, f"Error occurred while creating course. {ex}"
        assert True

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
