from abc import ABC, abstractmethod


class Item(ABC):
    # TODO declare normalizer so ide doesn't complain everywhere
    def __init__(self) -> None:
        assert hasattr(self, "normalizer"), (
            "Data class must have normalizer declared in order "
            "to provide data in NormalModel form."
        )

    def __init_subclass__(cls, **kwargs):
        super.__init_subclass__()
        if getattr(cls, "normalizer", None) is not None:
            normalizer = cls.normalizer
            cls.normal_read = normalizer.norm_deco(cls.read)
            cls.normal_read_many = normalizer.norm_many_deco(cls.read_many)
            cls.normal_get_recently_modified = normalizer.norm_many_deco(
                cls.get_recently_modified
            )
            cls.normal_create = normalizer.denorm_deco(cls.create, include_id=False)
            cls.normal_update = normalizer.denorm_deco(cls.update, include_id=True)
            normalizer.normal_model.add_source_item(cls)

    def name(self):
        return self.__class__.__name__

    # TODO create a subclass or mixin for last synced timestamp
    # not every use case may need it, such as event based syncing
    @property
    def last_synced_timestamp(self):
        data_store = self.normalizer.data_store
        timestamp = data_store.get_item_last_synced_time(self.name())

        return timestamp

    @last_synced_timestamp.setter
    def last_synced_timestamp(self, value):
        self.normalizer.data_store.set_item_last_synced_time(self.name(), value)

    @abstractmethod
    def get_recently_modified(self) -> list:
        pass

    @abstractmethod
    def read(self, item_id):
        pass

    @abstractmethod
    def read_many(self):
        pass

    @abstractmethod
    def create(self, data) -> str:
        """Must return the ID of the new item as a string."""
        pass

    @abstractmethod
    def update(self, data) -> str:
        """Must return the ID of the new item as a string."""
        pass

    @abstractmethod
    def delete(self, data):
        pass

    @abstractmethod
    def mark_as_synced(self, data):
        pass


class APIItem(Item):
    def __init__(self) -> None:
        super().__init__()
        assert hasattr(self, "path"), (
            "APIItem must have a path declared for making " "API requests to it."
        )

    @abstractmethod
    def get_recently_modified(self) -> list:
        pass

    def name(self):
        return self.__class__.__name__

    @abstractmethod
    def read(self, item_id):
        pass

    @abstractmethod
    def read_many(self):
        pass

    @abstractmethod
    def create(self, data) -> str:
        """Must return the ID of the new item."""
        pass

    @abstractmethod
    def update(self, data):
        pass

    @abstractmethod
    def delete(self, item_id):
        pass
