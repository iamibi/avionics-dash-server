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

# Local Modules
from .platform_service import PlatformService

logger = logging.getLogger(__name__)


class PlatformHelper:
    services: PlatformService = None

    def __init__(self) -> None:
        self.services = PlatformService()

    def get_user(self, user_id: str) -> Optional[Dict]:
        if Util.is_email_id(user_id) is True:
            email_id = Util.check_email(email_id=user_id)

            try:
                user_obj = self.services.user_service.by_email(email_id=email_id)
                return None if user_obj is None else user_obj.api_serialize()
            except Exception as ex:
                logger.error("Error fetching user from DB", ex)
                raise exc.AvionicsDashError("Invalid UserID passed!")
        elif Util.is_bson_id(user_id) is True:
            bson_id = ObjectId(oid=user_id)

            try:
                user_obj = self.services.user_service.by_id(user_id=bson_id)
                return None if user_obj is None else user_obj.api_serialize()
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
        user_obj = self.__validate_user_register(user_data=user_data)

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

    def get_module(self, module_id: str) -> Optional[Dict]:
        raise NotImplementedError

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
        raise NotImplementedError

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
        first_name = str(user_data["first_name"])
        last_name = str(user_data["last_name"])
        password = str(user_data["password"])
        confirm_password = str(user_data["confirm_password"])

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
        phone_number = str(user_data["phone"])
        if Util.is_phone_number_valid(phone_number) is False:
            raise exc.ValidationError(f"Invalid phone number passed!")

        address = str(user_data["address"])
        if 0 < len(address) <= cs.Limits.ADDRESS_LIMIT:
            raise exc.ValidationError(f"Address length is greater than {cs.Limits.ADDRESS_LIMIT}")

        role = str(user_data["role"])
        if role not in cs.Roles.VALID_USER_ROLES:
            raise exc.ValidationError(f"Invalid Role value passed!")

        logger.info(f"User {email_id} validation success!")

        return {
            "email": email_id,
            "password": password,
            "first_name": first_name,
            "last_name": last_name,
            "gender": gender,
            "dob": dob,
            "phone": phone_number,
            "address": address,
            "role": role,
        }


# Create a single instance
platform_helper = PlatformHelper()
