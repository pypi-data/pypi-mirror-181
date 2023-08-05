from datetime import datetime, timezone, timedelta

from nosql import no_sql_factory
from nosql.base import BaseNosqlWrapper


class DataStore:
    def __init__(self, db: BaseNosqlWrapper = None) -> None:
        if db is None:
            self.db = no_sql_factory()
        else:
            self.db = db

    def get_normal_id(self, item_name, item_id, model):
        key = ".".join((item_name, "id"))
        all_ids = self.db.query(model.collection, key, item_id)

        if all_ids is None:
            normal_id = self.create_id_record(item_name, item_id, model)
        else:
            normal_id = all_ids["_id"]

        return normal_id

    def create_id_record(self, item_name, item_id, model):
        insert_result = self.db.create(model.collection, item_name, item_id)
        return insert_result.inserted_id

    def add_item_id(self, model, item_name, item_id):
        update_field = ".".join((item_name, "id"))
        update_result = self.db.update_value(
            model.collection, "_id", model.uuid, update_field, item_id
        )
        return update_result

    def get_item_id(self, model, item_name):
        all_ids = self.db.query(model.collection, "_id", model.uuid)
        if all_ids is None or all_ids.get(item_name) is None:
            return None
        return all_ids.get(item_name).get("id")

    def get_item_last_modified_time(self, model, item_name, item_id):
        query_field = ".".join((item_name, "id"))
        item_result = self.db.query(model.collection, query_field, item_id)

        return item_result.get("lastmodifiedbyzync")

    def get_model_last_modified_time(self, model, item_name):
        all_items = self.db.query(model.collection, "_id", model.uuid)
        if all_items is None or all_items.get(item_name) is None:
            return None
        return all_items.get(item_name).get("lastmodifiedbyzync")

    def set_item_last_modified_time(self, model, item_name, item_id, timestamp):
        query_field = ".".join((item_name, "id"))
        update_field = ".".join((item_name, "lastmodifiedbyzync"))
        update_result = self.db.update_value(
            model.collection,
            query_field=query_field,
            query_value=item_id,
            field=update_field,
            value=timestamp,
        )
        return update_result

    def get_item_last_synced_time(self, item_name):
        result = self.db.query("last_synced", "item", item_name)
        if result is None:
            # TODO let the user define how far back to go here
            time_result = (datetime.now(timezone.utc) - timedelta(days=1)).isoformat()
        else:
            time_result = result["last_synced_timestamp"]

        return time_result

    def set_item_last_synced_time(self, item_name, timestamp):
        update_result = self.db.create_or_update(
            "last_synced",
            query_field="item",
            query_value=item_name,
            field="last_synced_timestamp",
            value=timestamp,
        )

        return update_result
