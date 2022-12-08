# Third-Party Library
import pytest
from dateutil import parser
from tests.data import DataStore

# Custom Library
from avionics_dash_server.app import create_app
from avionics_dash_server.services.course_service import CourseService
from avionics_dash_server.services.module_service import ModuleService
from avionics_dash_server.services.assignment_service import AssignmentService


class TestApi:
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
        app = create_app()
        with app.test_client() as test_client:
            yield test_client
        data_store, data_store_course, data_store_modules, data_store_assignments = setup_and_teardown_class
        data_store.clean_up_collection()
        data_store_course.clean_up_collection()
        data_store_modules.clean_up_collection()
        data_store_assignments.clean_up_collection()

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
            "firstName": "Mike",
            "lastName": "Ross",
            "email": "abcd@abc.com",
            "password": "abcd1234",
            "confirmPassword": "abcd1234",
            "address": "100 North Tryon Street, Charlotte, NC 28255",
            "phoneNumber": "+18004321000",
            "role": "V",
            "dob": "1/1/2000",
            "gender": "M",
            "education": "Professional Masters",
            "facts": "I am creative!",
        }
        response = test_client.post(
            "/api/v1/auth/register", json={"data": user_data}, headers={"Content-Type": "application/json"}
        )

        assert response.status_code == 201
        assert "data" in response.json
        data = response.json["data"]
        all_keys = list(user_data.keys())
        all_keys.append("id")
        all_keys.append("course_ids")
        all_keys.remove("confirmPassword")
        all_keys.remove("password")
        assert sorted(tuple(data.keys())) == sorted(all_keys)

    def test_register_with_same_user(self, setup_and_teardown_func):
        test_client = setup_and_teardown_func
        self.create_user(test_client)
        user_data = {
            "firstName": "Mike",
            "lastName": "Ross",
            "email": "abcd@abc.com",
            "password": "abcd1234",
            "confirmPassword": "abcd1234",
            "address": "100 North Tryon Street, Charlotte, NC 28255",
            "phoneNumber": "+18004321000",
            "role": "V",
            "dob": "1/1/2000",
            "gender": "M",
            "education": "Professional Masters",
            "facts": "I am creative!",
        }
        response = test_client.post(
            "/api/v1/auth/register", json={"data": user_data}, headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 400

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

    def test_get_user(self, setup_and_teardown_func):
        test_client = setup_and_teardown_func
        self.create_user(test_client)

        # Login
        login_response = test_client.post(
            "/api/v1/auth/login",
            json={"email": "abcd@abc.com", "password": "abcd1234"},
            headers={"Content-Type": "application/json"},
        )
        assert login_response.status_code == 201
        assert "token" in login_response.json

        response = test_client.get(
            "/api/v1/users/abcd%40abc.com", headers={"Authorization": f"Bearer {login_response.json['token']}"}
        )

        assert response.status_code == 200
        assert "data" in response.json

        response = test_client.get(
            f"/api/v1/users/{response.json['data']['id']}",
            headers={"Authorization": f"Bearer {login_response.json['token']}"},
        )

        assert response.status_code == 200
        assert "data" in response.json

    def test_add_course_to_user_id(self, setup_and_teardown_func):
        test_client = setup_and_teardown_func
        course = self.create_course()
        user = self.create_user(test_client=test_client)

        # Get a token
        login_response = test_client.post(
            "/api/v1/auth/login",
            json={"email": "abcd@abc.com", "password": "abcd1234"},
            headers={"Content-Type": "application/json"},
        )

        # Add the course to the user
        response = test_client.put(
            f"/api/v1/courses/{course.identifier}/add/{user['id']}",
            headers={"Authorization": f"Bearer {login_response.json['token']}", "Content-Type": "application/json"},
        )

        assert response.status_code == 204
        assert response.text == ""

        response = test_client.get(
            f"/api/v1/users/{user['id']}",
            headers={"Authorization": f"Bearer {login_response.json['token']}"},
        )

        assert response.status_code == 200
        assert "data" in response.json
        data = response.json["data"]
        assert len(data["course_ids"]) == 1
        assert str(course.identifier) in data["course_ids"]

    def test_get_courses_for_user_id(self, setup_and_teardown_func):
        test_client = setup_and_teardown_func
        course = self.create_course()
        user = self.create_user(test_client=test_client)

        # Get a token
        login_response = test_client.post(
            "/api/v1/auth/login",
            json={"email": "abcd@abc.com", "password": "abcd1234"},
            headers={"Content-Type": "application/json"},
        )

        # Add the course to the user
        response = test_client.put(
            f"/api/v1/courses/{course.identifier}/add/{user['id']}",
            headers={"Authorization": f"Bearer {login_response.json['token']}", "Content-Type": "application/json"},
        )

        assert response.status_code == 204
        assert response.text == ""

        response = test_client.get(
            f"/api/v1/users/{user['id']}/courses",
            headers={"Authorization": f"Bearer {login_response.json['token']}", "Content-Type": "application/json"},
        )

        assert response.status_code == 200
        assert "data" in response.json

    def test_get_user_with_courses(self, setup_and_teardown_func):
        test_client = setup_and_teardown_func
        course = self.create_course()
        user = self.create_user(test_client=test_client)

        # Get a token
        login_response = test_client.post(
            "/api/v1/auth/login",
            json={"email": "abcd@abc.com", "password": "abcd1234"},
            headers={"Content-Type": "application/json"},
        )
        assert login_response.status_code == 201

        # Add the course to the user
        response = test_client.put(
            f"/api/v1/courses/{course.identifier}/add/{user['id']}",
            headers={"Authorization": f"Bearer {login_response.json['token']}", "Content-Type": "application/json"},
        )

        assert response.status_code == 204

        response = test_client.get(
            "/api/v1/users/abcd%40abc.com", headers={"Authorization": f"Bearer {login_response.json['token']}"}
        )

        assert response.status_code == 200
        assert "data" in response.json

    @classmethod
    def create_course(cls):
        module = cls.create_module()
        assignment = cls.create_assignment()
        course_service = CourseService()

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
        assert True

        return course_service.by_title(course_title=course_obj["title"])

    @classmethod
    def create_user(cls, test_client):
        user_data = {
            "firstName": "Mike",
            "lastName": "Ross",
            "email": "abcd@abc.com",
            "password": "abcd1234",
            "confirmPassword": "abcd1234",
            "address": "100 North Tryon Street, Charlotte, NC 28255",
            "phoneNumber": "+18004321000",
            "role": "V",
            "dob": "1/1/2000",
            "gender": "M",
            "education": "Professional Masters",
            "facts": "I am creative!",
        }
        response = test_client.post(
            "/api/v1/auth/register", json={"data": user_data}, headers={"Content-Type": "application/json"}
        )

        assert response.status_code == 201
        assert "data" in response.json

        return response.json["data"]

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
            assert False, f"Error while fetching module. {ex}"

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
            assert False, f"Error while fetching assignment. {ex}"
