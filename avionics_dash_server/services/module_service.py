# Standard Library
from typing import Dict, List, Optional

# Third-Party Library
import pymongo
from bson import ObjectId

# Custom Library
from avionics_dash_server.util.util import Util
from avionics_dash_server.config.settings import settings
from avionics_dash_server.models.course_model import Module

# Local Modules
from .database_service import DatabaseService


class ModuleService(DatabaseService):
    def __init__(self) -> None:
        super(ModuleService, self).__init__()
        self._collection = self._db[settings.db.avionics_dash.collections.modules]
        self.index(mapping=[("name", pymongo.ASCENDING)], unique=True)

    def create_module(self, module: Dict) -> None:
        current_time = Util.utc_now()
        module["created_at"] = module["updated_at"] = current_time
        self.insert_one(doc=module)

    def by_id(self, module_id: ObjectId) -> Optional[Module]:
        module = self.find_one_by_id(bson_id=module_id)
        return self.__convert_to_module_obj(module)

    def by_ids(self, module_ids: List[ObjectId]) -> Optional[List[Module]]:
        modules = self.find(filter_dict={"_id": {"$in": module_ids}})
        return [self.__convert_to_module_obj(module) for module in modules] if len(modules) > 0 else None

    def by_name(self, module_name: str) -> Optional[Module]:
        module = self.find_one(filter_dict={"name": module_name})
        return self.__convert_to_module_obj(module)

    @classmethod
    def __convert_to_module_obj(cls, module: Optional[Dict]) -> Module:
        module_obj = None
        if module is not None:
            module["identifier"] = module["_id"]
            del module["_id"]
            module_obj = Module.parse_obj(module)
        return module_obj
