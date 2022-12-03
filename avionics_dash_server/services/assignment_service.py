# Standard Library
from typing import Dict, Optional

# Third-Party Library
import pymongo
from bson import ObjectId

# Custom Library
from avionics_dash_server.util.util import Util
from avionics_dash_server.config.settings import settings
from avionics_dash_server.models.assignment_model import Assignment

# Local Modules
from .database_service import DatabaseService


class AssignmentService(DatabaseService):
    def __init__(self):
        super(AssignmentService, self).__init__()
        self._collection = self._db[settings.db.avionics_dash.collections.assignments]
        self.index(mapping=[("name", pymongo.ASCENDING)], unique=True)

    def create_assignment(self, assignment: Dict) -> None:
        current_time = Util.utc_now()
        assignment["created_at"] = assignment["updated_at"] = current_time
        self.insert_one(doc=assignment)

    def by_id(self, assignment_id: ObjectId) -> Optional[Assignment]:
        assignment = self.find_one_by_id(bson_id=assignment_id)
        return self.__convert_to_assignment_obj(assignment)

    def by_name(self, assignment_name: str) -> Optional[Assignment]:
        assignment = self.find_one(filter_dict={"name": assignment_name})
        return self.__convert_to_assignment_obj(assignment)

    @classmethod
    def __convert_to_assignment_obj(cls, assignment: Optional[Dict]) -> Optional[Assignment]:
        assignment_obj = None
        if assignment is not None:
            assignment["identifier"] = assignment["_id"]
            del assignment["_id"]
            assignment_obj = Assignment.parse_obj(assignment)
        return assignment_obj
