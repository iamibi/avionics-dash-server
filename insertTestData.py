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

test_users = [
    {"_id": "1", "fname": "Tyler", "lname": "Johnson", "role": "STUDENT", "courses": ["1", "2"]},
    {"_id": "2", "fname": "Ibi", "lname": "Smith", "role": "STUDENT", "courses": ["2"]},
    {"_id": "3", "fname": "Disha", "lname": "Spock", "role": "TEACHER", "courses": ["1", "2"]},
]

try:
    result = users.insert_many(test_users)
    print("Inserted {} records to the users collection".format(len(result.inserted_ids)))
except(BulkWriteError):
    print("Users already exist. Skipping...")

test_courses = [
    {"_id": "1", "code": "GPS101", "name": "Intro to GPS Navigation", "students": ["1"], 
        "teachers": ["3"], "media": ["1", "3"]},
    {"_id": "2", "code": "FLY101", "name": "Intro to Basic Flight", "students": ["1", "2"], 
        "teachers": ["3"], "media": ["2", "4", "5"]}
]
try:
    result = courses.insert_many(test_courses)
    print("Inserted {} records to the courses collection".format(len(result.inserted_ids)))
except(BulkWriteError):
    print("Courses already exist. Skipping...")

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
