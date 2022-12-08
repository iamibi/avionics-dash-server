# Third-Party Library
import pymongo
from dateutil import parser
from bson.objectid import ObjectId

# Custom Library
from avionics_dash_server.services.user_service import UserService
from avionics_dash_server.services.course_service import CourseService
from avionics_dash_server.services.module_service import ModuleService
from avionics_dash_server.services.assignment_service import AssignmentService

user_service = UserService()
course_service = CourseService()
module_service = ModuleService()
assignment_service = AssignmentService()

user1_id = ObjectId()
user2_id = ObjectId()
user3_id = ObjectId()

course1_id = ObjectId()
course2_id = ObjectId()

asmnt1_id = ObjectId()
asmnt2_id = ObjectId()
asmnt3_id = ObjectId()


mod1_id = ObjectId()
mod2_id = ObjectId()

test_users = [
    {
        "_id": user1_id,
        "first_name": "Tyler",
        "last_name": "Johnson",
        "dob": parser.parse("10/01/1998"),
        "gender": "M",
        "email": "tjohnson@gmail.com",
        "role": "s",
        "address": "123 Sesame St.",
        "phone_number": "+18004321000",
        "password": "password",
        "course_ids": [ObjectId("639121637ca4efd619d0e85a"), ObjectId("639121637ca4efd619d0e85b")],
        "education": "Professional Masters",
        "facts": "I am creative!",
    },
    {
        "_id": user2_id,
        "first_name": "Ibi",
        "last_name": "Smith",
        "dob": parser.parse("05/03/1995"),
        "gender": "M",
        "email": "test_email@gmail.com",
        "role": "s",
        "address": "123 Garbage St.",
        "phone_number": "+18004321000",
        "password": "password",
        "course_ids": [ObjectId("639121637ca4efd619d0e85a")],
        "education": "Master of Science",
        "facts": "I am invincible!",
    },
    {
        "_id": user3_id,
        "first_name": "Disha",
        "last_name": "Spock",
        "dob": parser.parse("06/06/1998"),
        "gender": "F",
        "email": "spock123@gmail.com",
        "address": "123 Water St.",
        "phone_number": "935-439-2500",
        "role": "i",
        "password": "password",
        "course_ids": [ObjectId("639121637ca4efd619d0e85a"), ObjectId("639121637ca4efd619d0e85b")],
        "education": "PhD. Instructor",
        "facts": "I am available for help!",
    },
]

for user in test_users:
    try:
        user_service.create_user(user)
        print("Inserted 1 record to the users collection")
    except Exception as ex:
        print(f"Error inserting user. {ex}")

test_courses = [
    {
        "_id": course1_id,
        "img": "/images/course1.png",
        "title": "Intro to GPS Navigation",
        "price": "950",
        "desc": "First course to take",
        "modules": [mod1_id],
        "assignments": [asmnt1_id],
    },
    {
        "_id": course2_id,
        "img": "/images/course2.png",
        "title": "Intro to Basic Flight",
        "price": "950",
        "desc": "First course to take",
        "modules": [mod2_id],
        "assignments": [asmnt2_id],
    },
]

for course in test_courses:
    try:
        course_service.create_course(course)
    except Exception as ex:
        print(f"Error with course {ex}. Skipping...")

test_modules = [
    {
        "_id": mod1_id,
        "name": "module 1 name",
        "desc": "module 1 desc",
        "url": "https://www.youtube.com/watch?v=WZOk2Y65_5w&t=3s",
    },
    {
        "_id": mod2_id,
        "name": "module 2 name",
        "desc": "module 2 desc",
        "url": "https://www.youtube.com/watch?v=WZOk2Y65_5w&t=3s",
    },
]

for module in test_modules:
    try:
        module_service.create_module(module)
    except Exception as ex:
        print(f"Error with module {ex}. Skipping...")

test_assignments = [
    {
        "_id": asmnt1_id,
        "name": "Quiz 1",
        "desc": "Explain Principles of Flight with examples",
        "due": parser.parse("23/12/2022"),
        "points": "15",
        "submitted": False,
        "grade": "NA",
    },
    {
        "_id": asmnt2_id,
        "name": "Discussion 1",
        "desc": "Explain Principles of Flight with examples",
        "due": parser.parse("22/11/2022"),
        "points": "15",
        "submitted": False,
        "grade": "NA",
    },
    {
        "_id": asmnt3_id,
        "name": "Project 1",
        "desc": "Explain Principles of Flight with examples",
        "due": parser.parse("10/10/2019"),
        "points": "15",
        "submitted": False,
        "grade": "NA",
    },
]

for assignment in test_assignments:
    try:
        assignment_service.create_assignment(assignment)
    except Exception as ex:
        print(f"Error with assignment {ex}. Skipping...")
