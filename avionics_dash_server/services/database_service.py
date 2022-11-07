# Third-Party Library
from pymongo import MongoClient, database, collection

# Custom Library
from avionics_dash_server.common import exceptions as exs
from avionics_dash_server.config.settings import settings


class DatabaseService:
    db: database.Database = None
    collection: collection.Collection = None

    def __init__(self) -> None:
        db_name = settings.db.avionics_dash.db_name
        client = MongoClient(
            host=settings.db.avionics_dash.host,
            port=settings.db.avionics_dash.port,
            tz_aware=True,
            username=settings.credentials.db.username,
            password=settings.credentials.db.password,
            authSource=db_name,
            authMechanism=settings.db.avionics_dash.auth_mechanism,
        )
        self.db = client[db_name]

    def create_index(self):
        raise NotImplementedError

    def insert(self):
        raise NotImplementedError

    def find(self):
        raise NotImplementedError

    def update(self):
        raise NotImplementedError

    def __is_collection_set(self):
        if self.collection is None:
            raise exs.DbCollectionNotSet
