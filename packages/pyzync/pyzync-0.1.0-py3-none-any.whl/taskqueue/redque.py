from rq import Queue
from redis import Redis
from .base import TaskQueue


class RQ(TaskQueue):
    def __init__(self, host, port, password) -> None:
        my_connection = Redis(host=host, port=port, password=password)
        self._q = Queue(connection=my_connection)

    def produce_task(self, func, *args):
        # sync_fqn = "zync.sync.sync_model"
        self._q.enqueue(func, *args)
