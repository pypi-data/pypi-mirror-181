from taskqueue.base import task_queue_factory
from .config import Config
from .registry import build_registry, import_items
from .sync import sync_recent_from_item


class Zync:
    def __init__(self, config: Config):
        self.item_classes = []

        self.queue = task_queue_factory(config.task_queue)

        # Find the items!
        self.item_classes = import_items(config.items)
        self.registry = build_registry(self.item_classes)

    def run(self):
        for item in self.item_classes:
            self.queue.produce_task(sync_recent_from_item, item, self.registry)
