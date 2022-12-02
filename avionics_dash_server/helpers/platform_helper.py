# Standard Library
import logging
from typing import Any, Dict

# Third-Party Library
from bson import ObjectId

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

    def get_user(self, user_id: str):
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
                user_obj = self.services.user_service.by_id(bson_id=bson_id)
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
            raise exc.ValidationError("User not found!")

        try:
            return self.services.user_service.verify_user_password(
                retrieved_hash=user_obj.password.password_hash, provided_password=password
            )
        except Exception as ex:
            logger.error("Error occurred while checking the password", ex)
            raise exc.ValidationError("Authentication Failed!")

    def register_user(self, user_data: Dict[str, Any]):
        user_obj = self.__validate_user_register(user_data=user_data)

        try:
            self.services.user_service.create_user(user_obj)
        except exc.AvionicsDashError:
            raise exc.AvionicsDashError("Error occurred while creating the user!")

        return self.get_user(user_obj["email"])

    def __validate_user_register(self, user_data) -> Dict[str, Any]:
        if "email" not in user_data:
            raise exc.ValidationError("No Email Passed!")

        # Check whether the user already exists
        user = self.get_user(user_id=user_data["email"])
        if user is not None:
            raise exc.UserAlreadyExistsError

        # Perform validations on the received data
        email = Util.check_email(email_id=user_data["email"])
        first_name = user_data["first_name"]
        last_name = user_data["last_name"]
        password = user_data["password"]

        for name in (first_name, last_name):
            if not name.isalpha():
                raise exc.ValidationError("Invalid Name Passed!")
            if not 0 < len(name) <= cs.Limits.USER_NAME_LIMIT:
                raise exc.ValidationError(
                    f"Invalid Name length passed. It should be less than {cs.Limits.USER_NAME_LIMIT}"
                )

        if not 0 < len(password) <= cs.Limits.PASSWORD_LENGTH_LIMIT:
            raise exc.ValidationError(f"Please provide a password less than {cs.Limits.PASSWORD_LENGTH_LIMIT}")

        logger.info(f"User {email} validation success!")

        return {
            "email": email,
            "password": password,
            "first_name": first_name,
            "last_name": last_name,
        }


# Create a single instance
platform_helper = PlatformHelper()
