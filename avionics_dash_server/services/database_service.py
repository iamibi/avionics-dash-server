# Standard Library
from typing import Any, Dict, List, Union

# Third-Party Library
from pymongo import MongoClient, errors, database, collection

# Custom Library
from avionics_dash_server.common import exceptions as exs
from avionics_dash_server.config.settings import settings


class DatabaseService:
    _db: database.Database = None
    _collection: collection.Collection = None

    def __init__(self) -> None:
        db_name = settings.db.avionics_dash.db_name
        client = MongoClient(
            host=settings.db.avionics_dash.host,
            port=settings.db.avionics_dash.port,
            tz_aware=True,
        )
        self._db = client[db_name]

    def index(self, *, mapping: Union[str, List], unique: bool = False, background: bool = False) -> bool:
        self.__is_collection_set()

        operation = {"keys": mapping}
        if unique is True:
            operation["unique"] = True
        if background is True:
            operation["background"] = True

        try:
            self._collection.create_index(**operation)
        except errors.PyMongoError as py_err:
            raise exs.DatabaseError("Index Creation failed!") from py_err
        return True

    def insert_one(self, *, doc: Dict) -> None:
        self.__is_collection_set()

        try:
            response = self._collection.insert_one(document=doc)
        except errors.PyMongoError as py_err:
            raise exs.DatabaseError("Error occurred while performing insert_one!") from py_err

        if not response.acknowledged:
            raise exs.DatabaseError("insert_one query failed internally!")

    def insert_many(self, *, docs: List[Dict[str, Any]]) -> None:
        self.__is_collection_set()

        try:
            response = self._collection.insert_many(documents=docs)
        except errors.PyMongoError as py_err:
            raise exs.DatabaseError("Error occurred while performing insert_many!") from py_err

        if not response.acknowledged:
            raise exs.DatabaseError("insert_many query failed internally!")

    def find_one(self, *, filter_dict) -> Dict:
        self.__is_collection_set()

        try:
            return self._collection.find_one(filter=filter_dict)
        except errors.PyMongoError as py_err:
            raise exs.DatabaseError("Error occurred while performing find_one!") from py_err

    def find(self, *, filter_dict: Dict) -> List:
        self.__is_collection_set()

        try:
            response = self._collection.find(filter=filter_dict)
        except errors.PyMongoError as py_err:
            raise exs.DatabaseError("Error occurred while performing find!") from py_err

        return list(response)

    def __is_collection_set(self):
        if self._collection is None:
            raise exs.DbCollectionNotSet
