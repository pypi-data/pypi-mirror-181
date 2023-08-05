import os
from abc import ABC, abstractmethod


class TaskQueueConfig:
    def __init__(self):
        self.tq_type = os.environ.get("TASK_QUEUE")
        self.host = os.environ.get("TASK_HOST")
        self.port = int(os.environ.get("TASK_PORT"))
        self.password = os.environ.get("TASK_PASSWORD")


class TaskQueue(ABC):
    @abstractmethod
    def produce_task(self, func, *args):
        pass


def task_queue_factory(config: TaskQueueConfig = None) -> TaskQueue:
    if config is None:
        config = TaskQueueConfig()
    # TODO use a switch case
    if config.tq_type == "RQ":
        from .redque import RQ

        task_queue = RQ(config.host, config.port, config.password)
    else:
        raise Exception("RQ is currently the only supported task queue")

    return task_queue


# TODO task queue and nosql use the same strategies
# abstract out these strategies
