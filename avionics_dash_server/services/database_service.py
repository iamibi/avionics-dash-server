# Third-Party Library
from pymongo import MongoClient, database


class DatabaseService:
    _db: database.Database = None

    def __init__(self) -> None:
        client = MongoClient(host="localhost", port=27017, tz_aware=True)
        self._db = client["avionics_dash_dev"]

    def _create_index(self):
        raise NotImplementedError

    def _insert(self):
        raise NotImplementedError

    def _find(self):
        raise NotImplementedError

    def _update(self):
        raise NotImplementedError
