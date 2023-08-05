import os
from abc import ABC, abstractmethod

from dotenv import load_dotenv

load_dotenv()


class NosqlConfig:
    # TODO make this a dataclass
    def __init__(self):
        # TODO make db_type enumerable
        self.db_type = os.environ.get("NOSQL_DATABASE")
        self.host = os.environ.get("NOSQL_HOST")
        self.port = int(os.environ.get("NOSQL_PORT"))
        self.user = os.environ.get("NOSQL_USER")
        self.password = os.environ.get("NOSQL_PASSWORD")


class BaseNosqlWrapper(ABC):
    @abstractmethod
    def create(self, collection_name, field, value):
        pass

    @abstractmethod
    def query(self, collection_name, field, value):
        pass

    @abstractmethod
    def update_value(self, collection_name, query_field, query_value, field, value):
        pass

    @abstractmethod
    def create_or_update(self, collection_name, query_field, query_value, field, value):
        pass


def no_sql_factory(config: NosqlConfig = None) -> BaseNosqlWrapper:
    if config is None:
        config = NosqlConfig()
    if config.db_type == "Mongo":
        from nosql import Mongo

        db = Mongo(config.host, config.port, config.user, config.password)
    else:
        raise Exception("Only Mongo is currently supported")

    return db
