from avionics_dash_server.config.settings import settings

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
    {"_id": "1", "name": "Tyler", "role": "STUDENT", "courses": ["1", "2"]},
    {"_id": "2", "name": "Ibi", "role": "STUDENT", "courses": ["2"]},
    {"_id": "3", "name": "Disha", "role": "TEACHER", "courses": ["1", "2"]},
]

result = users.insert_many(test_users)
print("Inserted {} records to the users collection".format(result))

test_courses = [
    {"_id": "1", "code": "GPS101", "name": "Intro to GPS Navigation", "students": ["1"], 
        "teachers": ["3"]},
    {"_id": "2", "code": "FLY101", "name": "Intro to Basic Flight", "students": ["1", "2"], 
        "teachers": ["3"]}
]

result = courses.insert_many(test_courses)
print("Inserted {} records to the courses collection".format(result))

test_assignments = [
    {"_id": "1", "name": "Quiz 1", "type": "PERSONAL", "course": "GPS101"},
    {"_id": "2", "name": "Discussion 1", "type": "DISCUSSION", "course": "GPS101"},
    {"_id": "3", "name": "Project 1", "type": "GROUP", "course": "FLY101"}
]
result = assignments.insert_many(test_assignments)
print("Inserted {} records to the assignments collection".format(result))
