# Standard Library
import logging
from typing import Any, Dict, List, Union, Optional

# Third-Party Library
from bson import ObjectId
from dateutil import parser

# Custom Library
from avionics_dash_server.common import constants as cs
from avionics_dash_server.common import exceptions as exc
from avionics_dash_server.util.util import Util
from avionics_dash_server.models.user_model import User

# Local Modules
from .platform_service import PlatformService

logger = logging.getLogger(__name__)


class PlatformHelper:
    services: PlatformService = None

    def __init__(self) -> None:
        self.services = PlatformService()

    def get_user(self, user_id: str, serialize: bool = True) -> Union[None, Dict, User]:
        if Util.is_email_id(user_id) is True:
            email_id = Util.check_email(email_id=user_id)

            try:
                user_obj = self.services.user_service.by_email(email_id=email_id)
                return self.__get_user_obj(user_obj=user_obj, serialize=serialize)
            except Exception as ex:
                logger.error("Error fetching user from DB", ex)
                raise exc.AvionicsDashError("Invalid UserID passed!")
        elif Util.is_bson_id(user_id) is True:
            bson_id = ObjectId(oid=user_id)

            try:
                user_obj = self.services.user_service.by_id(user_id=bson_id)
                return self.__get_user_obj(user_obj=user_obj, serialize=serialize)
            except Exception as ex:
                logger.error("Error fetching usr from DB", ex)
                raise exc.AvionicsDashError("Invalid UserID passed!")

        raise exc.ValidationError("Invalid UserID passed!")

    def authenticate_user(self, email: str, password: str) -> bool:
        try:
            user_obj = self.services.user_service.by_email(email_id=email, with_pass=True)
        except Exception as ex:
            logger.error("Error fetching user from DB", ex)
            raise exc.ValidationError("Something went wrong!")

        if user_obj is None:
            logger.warning(f"User {email} not found!")
            raise exc.ValidationError("User not found!")

        try:
            return self.services.user_service.verify_user_password(
                retrieved_hash=user_obj.password.password_hash, provided_password=password
            )
        except Exception as ex:
            logger.error("Error occurred while checking the password", ex)
            raise exc.ValidationError("Authentication Failed!")

    def register_user(self, user_data: Dict[str, Any]) -> Optional[Dict]:
        try:
            user_obj = self.__validate_user_register(user_data=user_data)
        except exc.UserAlreadyExistsError:
            raise
        except Exception as ex:
            logger.error(f"Validation Failed with error.", ex)
            raise exc.ValidationError("Validation Failed!")

        try:
            self.services.user_service.create_user(user_obj)
        except exc.AvionicsDashError:
            raise exc.AvionicsDashError("Error occurred while creating the user!")

        return self.get_user(user_obj["email"])

    def get_course(self, course_id: str) -> Optional[Dict]:
        if Util.is_bson_id(identifier=course_id) is True:
            course_id = Util.get_id(course_id)
            logger.info(f"Fetching data for course id {course_id}")

            try:
                course = self.services.course_service.by_id(course_id=course_id)
            except Exception as ex:
                logger.error(f"Failed to fetch course data for {course_id}", ex)
                raise exc.AvionicsDashError("Error occurred while fetching the course!")

            # Fetch respective modules and assignments
            if course is not None:
                serialized = course.api_serialize()
                if len(course.modules) > 0:
                    modules = self.get_modules(module_ids=course.modules)
                    serialized["modules"] = modules
                if len(course.assignments) > 0:
                    assignments = self.get_assignments(assignment_ids=course.assignments)
                    serialized["assignments"] = assignments
                return serialized

        raise exc.ValidationError("Invalid Course ID passed!")

    def get_courses_for_user_id(self, user_id: str) -> Optional[List[Dict]]:
        user = self.get_user(user_id=user_id, serialize=False)
        logger.info(f"Fetching courses for user {user.identifier}")

        if user is None:
            raise exc.AvionicsDashError("User not found!")

        if not len(user.course_ids) > 0:
            return []

        courses = []
        try:
            for course_id in user.course_ids:
                course = self.get_course(course_id=str(course_id))
                courses.append(course)
        except exc.ValidationError:
            raise
        except exc.AvionicsDashError:
            raise
        except Exception as ex:
            logger.error(f"Error occurred while fetching course for user {user_id}", ex)
            raise exc.AvionicsDashError("Unable to fetch the course for the user!")
        return courses

    def update_user_with_course(self, user_id: str, course_id: str) -> None:
        if Util.is_bson_id(user_id) is False or Util.is_bson_id(course_id) is False:
            raise exc.ValidationError("Invalid UserId or CourseId passed!")

        user_id = Util.get_id(user_id)
        course_id = Util.get_id(course_id)
        try:
            user = self.services.user_service.by_id(user_id)
        except Exception as ex:
            logger.error(f"Error fetching user {user_id} from DB", ex)
            raise exc.AvionicsDashError("Invalid UserID passed!")

        if user is None:
            raise exc.ValidationError("Invalid UserID passed!")

        # If the course id is already present, then return
        if course_id in user.course_ids:
            return

        try:
            course = self.services.course_service.by_id(course_id)
        except Exception as ex:
            logger.error(f"Failed to fetch course data for {course_id}", ex)
            raise exc.AvionicsDashError("Error occurred while fetching the course!")

        if course is None:
            raise exc.ValidationError("Invalid CourseId Passed!")

        # Update the user with the course ID
        try:
            self.services.user_service.add_course_to_user(user_id=user_id, course_id=course_id)
        except Exception as ex:
            logger.error(f"Failed to add course data for {course_id} in user {user_id}", ex)
            raise exc.AvionicsDashError("Error occurred while adding the course to the user!")
        return

    def get_module(self, module_id: str) -> Optional[Dict]:
        module_id = Util.get_id(module_id)
        logger.info(f"Fetching module for {module_id}")

        try:
            module = self.services.module_service.by_id(module_id=module_id)
            if module is not None:
                return module.api_serialize()
        except Exception as ex:
            logger.error(f"Error occurred while fetching module!", ex)
            raise exc.AvionicsDashError("Unable to fetch module!")

    def get_modules(self, module_ids: List[Union[str, ObjectId]]) -> Optional[List[Dict]]:
        # Convert all the ids to a standard BSON Object ID
        module_ids = [Util.get_id(module_id) for module_id in module_ids]

        logger.info(f"Fetching modules for {module_ids}")

        try:
            modules = self.services.module_service.by_ids(module_ids=module_ids)
            if modules is not None:
                return [module.api_serialize() for module in modules]
        except Exception as ex:
            logger.error(f"Error occurred while fetching modules!", ex)
            raise exc.AvionicsDashError("Unable to fetch modules!")

    def get_assignment(self, assignment_id: str) -> Optional[Dict]:
        assignment_id = Util.get_id(assignment_id)
        logger.info(f"Fetching assignment for {assignment_id}")

        try:
            assignment = self.services.assignment_service.by_id(assignment_id=assignment_id)
            if assignment is not None:
                return assignment.api_serialize()
        except Exception as ex:
            logger.error(f"Error occurred while fetching assignment!", ex)
            raise exc.AvionicsDashError("Unable to fetch assignment!")

    def get_assignments(self, assignment_ids: List[Union[str, ObjectId]]) -> Optional[List[Dict]]:
        assignment_ids = [Util.get_id(assignment_id) for assignment_id in assignment_ids]

        logger.info(f"Fetching assignments for {assignment_ids}")

        try:
            assignments = self.services.assignment_service.by_ids(assignment_ids=assignment_ids)
            if assignments is not None:
                return [assignment.api_serialize() for assignment in assignments]
        except Exception as ex:
            logger.error(f"Error occurred while fetching assignments!", ex)
            raise exc.AvionicsDashError("Unable to fetch assignments!")

    def __validate_user_register(self, user_data) -> Dict[str, Any]:
        if "email" not in user_data:
            raise exc.ValidationError("No Email Passed!")

        # Check email id
        email_id = Util.check_email(email_id=str(user_data["email"]))

        # Check whether the user already exists
        user = self.get_user(user_id=email_id)
        if user is not None:
            raise exc.UserAlreadyExistsError

        # Perform validations on the received data
        first_name = str(user_data["firstName"])
        last_name = str(user_data["lastName"])
        password = str(user_data["password"])
        confirm_password = str(user_data["confirmPassword"])

        for name in (first_name, last_name):
            if not name.isalpha():
                raise exc.ValidationError("Invalid Name Passed!")
            if not 0 < len(name) <= cs.Limits.USER_NAME_LIMIT:
                raise exc.ValidationError(
                    f"Invalid Name length passed. It should be less than {cs.Limits.USER_NAME_LIMIT}"
                )

        if not 0 < len(password) <= cs.Limits.PASSWORD_LENGTH_LIMIT:
            raise exc.ValidationError(f"Please provide a password less than {cs.Limits.PASSWORD_LENGTH_LIMIT}")

        if password != confirm_password:
            raise exc.ValidationError("Password and Confirm Password don't match!")

        gender = str(user_data["gender"])
        if len(gender) != 1:
            raise exc.ValidationError(f"Invalid gender value passed!")

        dob = parser.parse(str(user_data["dob"]))
        phone_number = str(user_data["phoneNumber"])
        if Util.is_phone_number_valid(phone_number) is False:
            raise exc.ValidationError(f"Invalid phone number passed!")

        address = str(user_data["address"])
        if not 0 < len(address) <= cs.Limits.ADDRESS_LIMIT:
            raise exc.ValidationError(f"Address length is greater than {cs.Limits.ADDRESS_LIMIT}")

        role = str(user_data["role"]).lower()
        if role != cs.Roles.UserRole.VISITOR.value:
            raise exc.ValidationError("Invalid Role value passed!")
        role = cs.Roles.UserRole.STUDENT.value

        education = str(user_data["education"])
        if not 0 < len(education) < cs.Limits.EDUCATION_STR_LIMIT:
            raise exc.ValidationError("Invalid Education Value Passed!")

        facts = str(user_data["facts"])
        if not 0 < len(facts) < cs.Limits.FACTS_STR_LIMIT:
            raise exc.ValidationError("Invalid Facts value passed!")

        logger.info(f"User {email_id} validation success!")

        return {
            "email": email_id,
            "password": password,
            "first_name": first_name,
            "last_name": last_name,
            "gender": gender,
            "dob": dob,
            "phone_number": phone_number,
            "address": address,
            "role": role,
            "course_ids": [],
            "education": education,
            "facts": facts,
        }

    @classmethod
    def __get_user_obj(cls, user_obj: Optional[User], serialize: bool) -> Union[None, Dict, User]:
        if user_obj is None:
            return None
        elif serialize is True:
            return user_obj.api_serialize()
        return user_obj


# Create a single instance
platform_helper = PlatformHelper()
