import datetime
import user_model
from media_model import Media
from enums import AssignmentType

class Course:
    name: str
    students: List[Student]
    teachers: List[Teacher]
    assignments: List[Assignment]
    course_media: List[Media]

class Assignment:
    name: str
    description: str
    available: datetime
    due: datetime
    points: int
    assignment_type: AssignmentType 

class Submission:
    assignment: Assignment
    student: Student
    media: Media
    grade: int
    submitted: datetime