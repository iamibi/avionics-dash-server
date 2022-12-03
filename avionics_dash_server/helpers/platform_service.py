# Custom Library
from avionics_dash_server.common import exceptions as exc
from avionics_dash_server.services.user_service import UserService
from avionics_dash_server.services.course_service import CourseService
from avionics_dash_server.services.module_service import ModuleService
from avionics_dash_server.services.assignment_service import AssignmentService


class PlatformService:
    """Class to initialize all the services"""

    user_service: UserService = None
    assignment_service: AssignmentService = None
    course_service: CourseService = None
    module_service: ModuleService = None

    def __init__(self) -> None:
        try:
            self.user_service = UserService()
            self.assignment_service = AssignmentService()
            self.course_service = CourseService()
            self.module_service = ModuleService()
        except Exception as ex:
            raise exc.ServiceInitializationError("Unable to initialize the service.") from ex
