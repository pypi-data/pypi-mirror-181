from contextlib import contextmanager

from pymongo import MongoClient

from .base import BaseNosqlWrapper


class Mongo(BaseNosqlWrapper):
    def __init__(self, host="localhost", port=27017, user=None, password=None) -> None:
        # super().__init__()
        self.host = host
        self.port = port
        self.user = user
        self.password = password

    @contextmanager
    def client(self):
        mongo_client = MongoClient(
            host=self.host, port=self.port, username=self.user, password=self.password
        )
        yield mongo_client.zync
        mongo_client.close()

    def create(self, collection_name, item, item_id):
        with self.client() as db:
            collection = db[collection_name]
            result = collection.insert_one({item: {"id": item_id}})

        return result

    def query(self, collection_name, field, data):
        with self.client() as db:
            collection = db[collection_name]
            result = collection.find_one({field: data})

        return result

    def update_value(self, collection_name, query_field, query_value, field, value):
        with self.client() as db:
            collection = db[collection_name]
            query = {query_field: query_value}
            update_data = {"$set": {field: value}}
            result = collection.update_one(query, update_data)

        return result

    def create_or_update(self, collection_name, query_field, query_value, field, value):
        with self.client() as db:
            collection = db[collection_name]
            query = {query_field: query_value}
            update_data = {"$set": {field: value}}
            result = collection.update_one(query, update_data, upsert=True)

        return result
