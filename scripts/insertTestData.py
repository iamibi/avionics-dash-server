from avionics_dash_server.config.settings import settings
from pymongo.errors import BulkWriteError
import pymongo

myclient = pymongo.MongoClient(
    host=settings.db.avionics_dash.host,
    port=settings.db.avionics_dash.port
)

mydb = myclient[settings.db.avionics_dash.db_name]

users = mydb["users"]
courses = mydb["courses"]
assignments = mydb["assignments"]
media = mydb["media"]
modules = mydb["modules"]
messages = mydb["messages"]

test_users = [
    {"_id": "1", "first_name": "Tyler", "last_name": "Johnson", "dob": "10/01/1998", "email": "tjohnson@av-dash.edu", "role": "STUDENT", "password": "password", "courses": ["1", "2"]},
    {"_id": "2", "first_name": "Ibi", "last_name": "Smith", "dob": "10/01/1998", "email": "test_email@av-dash.edu", "role": "STUDENT","password": "password", "courses": ["2"]},
    {"_id": "3", "first_name": "Disha", "last_name": "Spock", "dob": "10/01/1998", "email": "spock123@av-dash.edu", "role": "TEACHER","password": "password", "courses": ["1", "2"]},
]

try:
    result = users.insert_many(test_users)
    print("Inserted {} records to the users collection".format(len(result.inserted_ids)))
except(BulkWriteError):
    print("Users already exist. Skipping...")

test_courses = [
    {"_id": "1", "code": "GPS101", "title": "Intro to GPS Navigation", "students": ["1"], 
        "teachers": ["3"], "modules": ["1"], "desc": "First course to take", "price": "950"},
    {"_id": "2", "code": "FLY101", "title": "Intro to Basic Flight", "students": ["1", "2"], 
        "teachers": ["3"], "modules": ["2"], "desc": "First course to take", "price": "950"}
]
try:
    result = courses.insert_many(test_courses)
    print("Inserted {} records to the courses collection".format(len(result.inserted_ids)))
except(BulkWriteError):
    print("Courses already exist. Skipping...")

test_modules = [
    {"_id": "1", "name": "module 1 name", "desc": "module 1 desc", "url": "courses/module1"},
    {"_id": "2", "name": "module 2 name", "desc": "module 2 desc", "url": "courses/module2"} 
]

try:
    result = modules.insert_many(test_modules)
    print("Inserted {} records to the modules collection".format(len(result.inserted_ids)))
except(BulkWriteError):
    print("Modules already exist. Skipping...")


test_assignments = [
    {"_id": "1", "name": "Quiz 1", "type": "PERSONAL", "course": "GPS101"},
    {"_id": "2", "name": "Discussion 1", "type": "DISCUSSION", "course": "GPS101"},
    {"_id": "3", "name": "Project 1", "type": "GROUP", "course": "FLY101"}
]

try:
    result = assignments.insert_many(test_assignments)
    print("Inserted {} records to the assignments collection".format(len(result.inserted_ids)))
except(BulkWriteError):
    print("Assignments already exist. Skipping...")
    
test_media = [
    {"_id": "1", "filetype": "pdf", "name": "GPS Map 1", "description": "A PDF map describing the GPS area", "path": "/media/gps-map-1.pdf"},
    {"_id": "2", "filetype": "mp4", "name": "Ignition Video 1", "description": "A video demonstrating ignition", "path": "/media/ignition-vid-1.mp4"},
    {"_id": "3", "filetype": "png", "name": "GPS Button Labels", "description": "An image of button labels on gps", "path": "/media/gps-buttons-1.png"},
    {"_id": "4", "filetype": "txt", "name": "Flight Instructions", "description": "How to fly a plane", "path": "/media/fly.txt"},
    {"_id": "5", "filetype": "mp3", "name": "Plane Sounds", "description": "Normal plane sounds", "path": "/media/plane-woosh.mp3"}
]

try:
    result = media.insert_many(test_media)
    print("Inserted {} records to the media collection".format(len(result.inserted_ids)))
except(BulkWriteError):
    print("Media already exists. Skipping...")


test_messages = [
    {"_id": "1", "from_user": "1", "subject": "First Message", "content": "Hi, this is my first message", "to_user": "2", "has_read": True},
    {"_id": "2", "from_user": "2", "subject": "Responding", "content": "Congrats!", "to_user": "1", "has_read": False}
]
try:
    result = messages.insert_many(test_messages)
    print("Inserted {} records to the messages collection".format(len(result.inserted_ids)))
except(BulkWriteError):
    print("Messages already exists. Skipping...")
