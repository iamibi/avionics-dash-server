# Standard Library
from typing import Dict, List, Optional

# Third-Party Library
import pymongo
from bson import ObjectId

# Custom Library
from avionics_dash_server.util.util import Util
from avionics_dash_server.config.settings import settings
from avionics_dash_server.models.course_model import Course

# Local Modules
from .database_service import DatabaseService


class CourseService(DatabaseService):
    def __init__(self) -> None:
        super(CourseService, self).__init__()
        self._collection = self._db[settings.db.avionics_dash.collections.courses]
        self.index(mapping=[("title", pymongo.ASCENDING)], unique=True)

    def create_course(self, course: Dict) -> None:
        current_time = Util.utc_now()
        course["updated_at"] = course["created_at"] = current_time
        self.insert_one(doc=course)

    def by_id(self, course_id: ObjectId) -> Optional[Course]:
        course = self.find_one_by_id(bson_id=course_id)
        return self.__convert_to_course_obj(course)

    def by_title(self, course_title: str) -> Optional[Course]:
        course = self.find_one(filter_dict={"title": course_title})
        return self.__convert_to_course_obj(course)

    def get_all(self) -> Optional[List[Course]]:
        courses = self.find(filter_dict={})
        if len(courses) == 0:
            return None
        return [self.__convert_to_course_obj(course) for course in courses]

    @classmethod
    def __convert_to_course_obj(cls, course: Dict) -> Course:
        course_obj = None
        if course is not None:
            course["identifier"] = course["_id"]
            del course["_id"]
            course_obj = Course.parse_obj(course)
        return course_obj
