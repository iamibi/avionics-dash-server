# Standard Library
import logging
from typing import Dict, Optional

# Custom Library
from avionics_dash_server.common import exceptions as exc
from avionics_dash_server.util.util import Util

# Local Modules
from .platform_service import PlatformService

logger = logging.getLogger(__name__)


class PlatformHelper:
    services: PlatformService = None

    def __init__(self) -> None:
        self.services = PlatformService()

    def get_user(self, email: str):
        email_id = Util.check_email(email_id=email)

        try:
            user = self.services.user_service.by_email(email_id=email_id)
        except Exception as ex:
            logger.error("Error fetching user from DB", ex)
            raise exc.AvionicsDashError("Something went wrong!")

        return user

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
                retrieved_hash=user_obj["password"]["password_hash"],
                provided_password=password
            )
        except Exception as ex:
            logger.error("Error occurred while checking the password", ex)
            raise exc.ValidationError("Authentication Failed!")

    def register_user(self, user_data: Dict):
        if "email" not in user_data:
            raise exc.ValidationError("No Email Passed!")

        user = self.get_user(email=user_data["email"])
        if user is not None:
            raise exc.UserAlreadyExistsError

        user_obj = {
            "email": user_data["email"],
            "password": user_data["password"],
            "first_name": user_data["first_name"],
            "last_name": user_data["last_name"],
        }

        try:
            self.services.user_service.create_user(user_obj)
        except exc.AvionicsDashError:
            raise exc.AvionicsDashError("Error occurred while creating the user!")


# Create a single instance
platform_helper = PlatformHelper()
