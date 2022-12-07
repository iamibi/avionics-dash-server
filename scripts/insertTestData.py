from avionics_dash_server.config.settings import settings
from avionics_dash_server.services.user_service import UserService
from pymongo.errors import BulkWriteError
from bson.objectid import ObjectId
import pymongo

myclient = pymongo.MongoClient(
    host=settings.db.avionics_dash.host,
    port=settings.db.avionics_dash.port
)

user_service = UserService()

mydb = myclient[settings.db.avionics_dash.db_name]

users = mydb["users"]
courses = mydb["courses"]
assignments = mydb["assignments"]
media = mydb["media"]
modules = mydb["modules"]
messages = mydb["messages"]

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

med1_id = ObjectId()
med2_id = ObjectId()
med3_id = ObjectId()
med4_id = ObjectId()
med5_id = ObjectId()

msg1_id = ObjectId()
msg2_id = ObjectId()

test_users = [
    {
        "_id": user1_id, 
        "first_name": "Tyler",
        "last_name": "Johnson",
        "dob": "10/01/1998",
        "gender": "male",
        "email": "tjohnson@av-dash.edu",
        "role": "STUDENT",
        "address": "123 Sesame St.",
        "phone_number": "123-456-7890",
        "password":"password",
        "courses": [course1_id, course2_id]
    },
    {
        "_id": user2_id,
        "first_name": "Ibi",
        "last_name": "Smith",
        "dob": "10/01/1998",
        "gender": "male",
        "email": "test_email@av-dash.edu",
        "role": "STUDENT",
        "address": "123 Garbage St.",
        "phone_number": "432-685-2498",
        "password": "password",
        "courses": [course2_id]
    },
    {
        "_id": user3_id,
        "first_name": "Disha",
        "last_name": "Spock",
        "dob": "10/01/1998",
        "gender": "female",
        "email": "spock123@av-dash.edu",
        "address": "123 Water St.",
        "phone_number": "935-439-2500",
        "role": "TEACHER",
        "password": "password",
        "courses": [course1_id, course2_id]
    }
]

for user in test_users:
    try:
        user_service.create_user(user)
        print("Inserted 1 record to the users collection")
    except:
        print("Error inserting user")

test_courses = [
    {
        "_id": course1_id,
        "img": "/images/course1.png",
        "title": "Intro to GPS Navigation",
        "price": "950",
        "desc": "First course to take",
        "modules": [mod1_id],
        "assignments": [asmnt1_id]
    },
    {
        "_id": course2_id,
        "img": "/images/course2.png",
        "title": "Intro to Basic Flight",
        "price": "950",
        "desc": "First course to take",
        "modules": [mod2_id],
        "assignments": [asmnt2_id]
    }
]
try:
    result = courses.insert_many(test_courses)
    print("Inserted {} records to the courses collection".format(len(result.inserted_ids)))
except(BulkWriteError):
    print("Courses already exist. Skipping...")

test_modules = [
    {"_id": mod1_id, "name": "module 1 name", "desc": "module 1 desc", "url": "courses/module1"},
    {"_id": mod2_id, "name": "module 2 name", "desc": "module 2 desc", "url": "courses/module2"} 
]

try:
    result = modules.insert_many(test_modules)
    print("Inserted {} records to the modules collection".format(len(result.inserted_ids)))
except(BulkWriteError):
    print("Modules already exist. Skipping...")


test_assignments = [
    {"_id": asmnt1_id, "name": "Quiz 1", "type": "PERSONAL", "course": "GPS101"},
    {"_id": asmnt2_id, "name": "Discussion 1", "type": "DISCUSSION", "course": "GPS101"},
    {"_id": asmnt3_id, "name": "Project 1", "type": "GROUP", "course": "FLY101"}
]

try:
    result = assignments.insert_many(test_assignments)
    print("Inserted {} records to the assignments collection".format(len(result.inserted_ids)))
except(BulkWriteError):
    print("Assignments already exist. Skipping...")
    
test_media = [
    {"_id": med1_id, "filetype": "pdf", "name": "GPS Map 1", "description": "A PDF map describing the GPS area", "path": "/media/gps-map-1.pdf"},
    {"_id": med2_id, "filetype": "mp4", "name": "Ignition Video 1", "description": "A video demonstrating ignition", "path": "/media/ignition-vid-1.mp4"},
    {"_id": med3_id, "filetype": "png", "name": "GPS Button Labels", "description": "An image of button labels on gps", "path": "/media/gps-buttons-1.png"},
    {"_id": med4_id, "filetype": "txt", "name": "Flight Instructions", "description": "How to fly a plane", "path": "/media/fly.txt"},
    {"_id": med5_id, "filetype": "mp3", "name": "Plane Sounds", "description": "Normal plane sounds", "path": "/media/plane-woosh.mp3"}
]

try:
    result = media.insert_many(test_media)
    print("Inserted {} records to the media collection".format(len(result.inserted_ids)))
except(BulkWriteError):
    print("Media already exists. Skipping...")


test_messages = [
    {"_id": msg1_id, "from_user": user1_id, "subject": "First Message", "content": "Hi, this is my first message", "to_user": user2_id, "has_read": True},
    {"_id": msg2_id, "from_user": user2_id, "subject": "Responding", "content": "Congrats!", "to_user": user1_id, "has_read": False}
]
try:
    result = messages.insert_many(test_messages)
    print("Inserted {} records to the messages collection".format(len(result.inserted_ids)))
except(BulkWriteError):
    print("Messages already exists. Skipping...")
