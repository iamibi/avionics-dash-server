# Custom Library
from avionics_dash_server.common import exceptions as exc
from avionics_dash_server.services.user_service import UserService


class PlatformService:
    """Class to initialize all the services"""

    user_service: UserService = None

    def __init__(self) -> None:
        try:
            self.user_service = UserService()
        except Exception as ex:
            raise exc.ServiceInitializationError(f"Unable to initialize the service.") from ex
