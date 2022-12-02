# Standard Library
import datetime

# Custom Library
from avionics_dash_server.common.constants import AssignmentType


class Assignment:
    name: str
    description: str
    available: datetime
    due: datetime
    points: int
    assignment_type: AssignmentType
