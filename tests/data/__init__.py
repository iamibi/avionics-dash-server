# Third-Party Library
from pymongo import MongoClient


class DataStore:
    __db = None
    __collection = None

    def __init__(self, collection_name: str):
        db_name = "avionics_dash_test"
        client = MongoClient(
            host="localhost",
            port=27017,
            tz_aware=True,
        )
        self.__db = client[db_name]
        self.__collection = self.__db.get_collection(name=collection_name)

    def clean_up_collection(self) -> int:
        deleted = self.__collection.delete_many({})
        return deleted.deleted_count

    def get_data_count(self):
        return self.__collection.count_documents({})
