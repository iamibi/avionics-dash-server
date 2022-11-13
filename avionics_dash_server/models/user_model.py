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
