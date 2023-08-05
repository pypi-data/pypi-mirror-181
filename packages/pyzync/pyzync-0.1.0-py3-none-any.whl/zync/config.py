from typing import List

from dotenv import load_dotenv

from nosql.base import NosqlConfig
from taskqueue.base import TaskQueueConfig

load_dotenv()


class Config:
    def __init__(
        self,
        items: List[str],
        db: NosqlConfig = None,
        task_queue: TaskQueueConfig = None,
    ):
        self.items = items

        if db is None:
            self.db = NosqlConfig()
        else:
            self.db = db

        if task_queue is None:
            self.task_queue = TaskQueueConfig()
        else:
            self.task_queue = task_queue
