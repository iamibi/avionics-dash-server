# Third-Party Library
from pymongo import MongoClient, database, collection

# Custom Library
from avionics_dash_server.config.settings import settings


class DatabaseService:
    _db: database.Database = None
    _collections: collection.Collection = None

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
        self._db = client[db_name]

    def _create_index(self):
        raise NotImplementedError

    def _insert(self):
        raise NotImplementedError

    def _find(self):
        raise NotImplementedError

    def _update(self):
        raise NotImplementedError
