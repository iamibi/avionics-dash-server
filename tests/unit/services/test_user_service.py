# Third-Party Library
import pytest
from dateutil import parser
from tests.data import DataStore

# Custom Library
from avionics_dash_server.models.user_model import User, PasswordModel
from avionics_dash_server.services.user_service import UserService
from avionics_dash_server.services.course_service import CourseService
from avionics_dash_server.services.module_service import ModuleService
from avionics_dash_server.services.assignment_service import AssignmentService


class TestUserService:
    @pytest.fixture(scope="class")
    def setup_and_teardown_class(self):
        data_store = DataStore(collection_name="users")
        data_store_course = DataStore(collection_name="courses")
        data_store_modules = DataStore(collection_name="modules")
        data_store_assignments = DataStore(collection_name="assignments")

        data_store.clean_up_collection()
        data_store_course.clean_up_collection()
        data_store_modules.clean_up_collection()
        data_store_assignments.clean_up_collection()

        yield data_store, data_store_course, data_store_modules, data_store_assignments

        data_store.clean_up_collection()
        data_store_course.clean_up_collection()
        data_store_modules.clean_up_collection()
        data_store_assignments.clean_up_collection()

    @pytest.fixture(scope="function")
    def setup_and_teardown_func(self, setup_and_teardown_class):
        user_service = UserService()
        yield user_service
        data_store, data_store_course, data_store_modules, data_store_assignments = setup_and_teardown_class
        data_store.clean_up_collection()
        data_store_course.clean_up_collection()
        data_store_modules.clean_up_collection()
        data_store_assignments.clean_up_collection()

    def test_user_service_init(self):
        user_service = UserService()
        assert user_service is not None

    def test_create_user(self, setup_and_teardown_func):
        user_service = setup_and_teardown_func

        user_obj = {
            "email": "abc@abc.com",
            "password": "abcd1234",
            "first_name": "Mike",
            "last_name": "Ross",
            "address": "100 North Tryon Street, Charlotte, NC 28255",
            "phone_number": "+18004321000",
            "role": "s",
            "dob": "1/1/2000",
            "gender": "M",
            "course_ids": [],
            "education": "Professional Masters",
            "facts": "I am creative!",
        }

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

        assert isinstance(user, User) is True
        assert user_obj["email"] == user.email

    def test_by_email_with_password(self, setup_and_teardown_func):
        user_service = setup_and_teardown_func

        user_obj = self.create_test_user(user_service)

        try:
            user = user_service.by_email(email_id="abc@abc.com", with_pass=True)
        except Exception as ex:
            assert False, f"Failed to fetch user. Error: {ex}"

        assert isinstance(user, User) is True
        assert user_obj["email"] == user.email
        assert isinstance(user.password, PasswordModel)

    def test_add_course_to_user(self, setup_and_teardown_func):
        user_service = setup_and_teardown_func
        course = self.create_courses()
        self.create_test_user(user_service)

        try:
            user = user_service.by_email(email_id="abc@abc.com")
        except Exception as ex:
            assert False, f"Failed to fetch user. Error: {ex}"

        try:
            user_service.add_course_to_user(user_id=user.identifier, course_id=course.identifier)
        except Exception as ex:
            assert False, f"Failed to add course to the user. Error: {ex}"

        try:
            user = user_service.by_email(email_id="abc@abc.com")
        except Exception as ex:
            assert False, f"Failed to fetch user. Error: {ex}"

        assert len(user.course_ids) == 1
        assert course.identifier in user.course_ids

    @classmethod
    def create_test_user(cls, user_service):
        user_obj = {
            "email": "abc@abc.com",
            "password": "abcd1234",
            "first_name": "Mike",
            "last_name": "Ross",
            "address": "100 North Tryon Street, Charlotte, NC 28255",
            "phone_number": "+18004321000",
            "role": "s",
            "dob": parser.parse("1/1/2000"),
            "gender": "M",
            "course_ids": [],
            "education": "Professional Masters",
            "facts": "I am creative!",
        }
        try:
            user_service.create_user(user_obj)
        except Exception as ex:
            assert False, f"Failed to create user. Error: {ex}"
        return user_obj

    @classmethod
    def create_courses(cls):
        course_service = CourseService()
        module = cls.create_module()
        assignment = cls.create_assignment()

        course_obj = {
            "img": "/courses/c1.jpeg",
            "title": "Private Pilot Made Easy Online Ground School",
            "price": "$890",
            "desc": "Our online ground school will help you pass the FAA Private Pilot test with flying colors. "
            "Achieve your dreams of flying an airplane.",
            "modules": [module.identifier],
            "assignments": [assignment.identifier],
        }

        try:
            course_service.create_course(course=course_obj)
        except Exception as ex:
            assert False, f"Error occurred while creating course. {ex}"

        try:
            return course_service.by_title(course_title=course_obj["title"])
        except Exception as ex:
            assert False, f"Error occurred while fetching the course. {ex}"

    @classmethod
    def create_module(cls):
        module_service = ModuleService()
        module_obj = {
            "name": "Becoming a Private Pilot",
            "desc": "What does it take to become a Private Pilot? You will know right after this module",
            "url": "https://www.youtube.com/watch?v=WZOk2Y65_5w&t=3s",
        }

        try:
            module_service.create_module(module_obj)
        except Exception as ex:
            assert False, f"Error while creating module. {ex}"

        try:
            return module_service.by_name(module_name=module_obj["name"])
        except Exception as ex:
            assert False, f"Error while fetching the module. {ex}"

    @classmethod
    def create_assignment(cls):
        assignment_service = AssignmentService()
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

        try:
            return assignment_service.by_name(assignment_name=assignment_obj["name"])
        except Exception as ex:
            assert False, f"Error while fetching the assignment. {ex}"
