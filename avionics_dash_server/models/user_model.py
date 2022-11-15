# Standard Library
from datetime import datetime

# Third-Party Library
from pydantic import BaseModel, validator

from typing import List
from course_model import Course

class User:
    fname: str
    lname: str
    email: str
    password: str

    def serialize(self):
        pass

    def fromDict(self):
        pass

class Student(User):
    role = 'student'
    courses: List[Course]

class Teacher(User):
    role = 'teacher'
    courses: List[Course]

class Admin(User):
    role = 'admin'

class PasswordModel(BaseModel):
    password_hash: str
    created_at: datetime
    updated_at: datetime

    @validator("created_at", "updated_at", pre=True, always=True)
    def check_timestamp(cls, v):
        # Check the timezone is UTC or not
        if v.tzname() != "UTC":
            return ValueError("The timezone is not in UTC format")
        return v
