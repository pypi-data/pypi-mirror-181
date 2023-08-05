import pprint
from datetime import datetime, timezone
from typing import Type

from taskqueue import task_queue_factory, TaskQueue
from . import Item
from . import NormalModel
from .data_store import DataStore


def sync_model(normal_model: NormalModel, item: Item, registry):
    data_store = DataStore()

    count = 0
    if not normal_model.check_sync_all(source=item):
        return count

    print("Normal model source items")
    pprint.pprint(registry[type(normal_model)])
    print("Current source")
    print(type(item))
    destinations = registry[type(normal_model)].difference({type(item)})
    # pprint.pprint("Model to be synced:")
    # pprint.pprint(normal_model)
    pprint.pprint("Syncing to:")
    pprint.pprint(destinations)

    for destination in destinations:
        sync_item = destination()
        item_name = sync_item.name()
        item_id = data_store.get_item_id(normal_model, item_name)

        # verify if the item should be synced or not
        if item_id is None:
            # Check if we should create to this destination
            if not normal_model.check_sync_to_destination(
                source=item, destination=destination, create=True
            ):
                continue

            # this returns the raw item data
            print("Running create to destination")
            destination_item_id = sync_item.normal_create(normal_model)
            data_store.add_item_id(normal_model, item_name, destination_item_id)
        else:
            if not normal_model.check_sync_to_destination(
                source=item, destination=destination, create=False
            ):
                continue
            print("Running update to destination")
            destination_item_id = sync_item.normal_update(normal_model)
        data_store.set_item_last_modified_time(
            normal_model, item_name, destination_item_id, datetime.now(timezone.utc)
        )
        count += 1
    item.mark_as_synced(normal_model)

    return count


def sync_data(data: dict, item: Item):
    normal_model = item.normalizer.normalize(data, item.read)
    result = sync_model(normal_model, item)

    return result


def sync_recent_from_item(
    item_class: Type[Item], registry, task_queue: TaskQueue = None
):
    data_store = DataStore()
    sync_timestamp = datetime.now(timezone.utc).isoformat()
    item = item_class()
    result = item.normal_get_recently_modified()

    if task_queue is None:
        task_queue = task_queue_factory()
    for data in result:
        pprint.pprint(data)
        # TODO compare timestamp in datastore with model
        stored_modified_timestamp = data_store.get_model_last_modified_time(
            data, item.name()
        ).replace(tzinfo=timezone.utc)

        if stored_modified_timestamp is not None:
            difference = data.last_modified - stored_modified_timestamp
            if difference.total_seconds() > 10:
                task_queue.produce_task(sync_model, data, item, registry)

    item.last_synced_timestamp = sync_timestamp


def sync_model_to_destination(
    normal_model: NormalModel, source: Item, destination: Item, force: bool = False
):
    data_store = DataStore()
    item_name = destination.name()
    item_id = data_store.get_item_id(normal_model, item_name)

    create = item_id is None
    result = None
    if force or normal_model.check_sync_to_destination(
        source=source, destination=destination, create=create
    ):
        # the result is the item id
        if create:
            result = destination.normal_create(normal_model)
            data_store.add_item_id(normal_model, item_name, result)
        else:
            result = destination.normal_update(normal_model)

    return result


def sync_data_to_destination(
    data: dict, source: Item, destination: Item, force: bool = False
):
    normal_model = source.normalizer.normalize(data, source.read)
    result = sync_model_to_destination(normal_model, source, destination, force)

    return result
