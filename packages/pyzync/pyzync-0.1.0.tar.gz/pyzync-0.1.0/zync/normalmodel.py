from abc import abstractmethod
from datetime import datetime
from typing import ClassVar

from bson.objectid import ObjectId
from pydantic import BaseModel

from . import Item


class NormalModel(BaseModel):
    # TODO make a validator for uuid
    uuid: ObjectId = None
    # TODO find a way to keep last_modified READ ONLY
    # it should never be denormalized into raw data
    # Only read for the purpose of comparing to zync's last modified timestamp
    last_modified: datetime = None
    collection: ClassVar[str]
    source_items: ClassVar[set] = set()

    @classmethod
    def add_source_item(cls, item):
        # validate that item is subclass of Item
        # validate that the item's normalizer converts to this normalmodel
        if issubclass(item, Item) and item.normalizer.normal_model is cls:
            cls.source_items.add(item)
        else:
            # TODO create appropriate exception
            raise Exception

    class Config:
        # TODO remove this after fixing ObjectId as a type
        arbitrary_types_allowed = True

    @abstractmethod
    def check_sync_all(self, source: Item) -> bool:
        pass

    @abstractmethod
    def check_sync_to_destination(
        self, source: Item, destination: Item, create: bool
    ) -> bool:
        pass
