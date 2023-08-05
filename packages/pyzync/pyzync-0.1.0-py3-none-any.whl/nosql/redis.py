from .base import BaseNosqlWrapper
import redis


class Redis(BaseNosqlWrapper):
    def __init__(self) -> None:
        self._client = self.connect()

    def connect(self):
        client = redis.Redis(host="localhost", port=12000, password="guest")
        return client

    def create(self, collection, field, value):
        pass

    def update_value(self, collection_name, query_field, query_value, field, value):
        pass

    def update_id(self, collection, uuid, item, value):
        pass
