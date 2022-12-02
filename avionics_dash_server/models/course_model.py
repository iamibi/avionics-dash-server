# Standard Library
import datetime
from typing import List

# Third-Party Library
from user_model import User
from media_model import Media
from assignment_model import Assignment

# Custom Library
from avionics_dash_server.common.constants import AssignmentType


class Course:
    name: str
    students: List[User]
    teachers: List[User]
    assignments: List[Assignment]
    course_media: List[Media]


class Submission:
    assignment: Assignment
    student: User
    media: Media
    grade: int
    submitted: datetime
