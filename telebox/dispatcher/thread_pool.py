from typing import Callable, Any

from threading import Thread
from queue import Queue


class ThreadPool:

    def __init__(self, threads: int):
        if threads < 1:
            raise ValueError("The number of threads cannot be less than 1!")

        self._threads = threads
        self._active_threads = []
        self._queue = Queue()

    def start_threads(self, target: Callable, args: tuple) -> None:
        threads = [
            Thread(target=target, args=args, daemon=True)
            for _ in range(self._threads)
        ]

        for i in threads:
            i.start()
            self._active_threads.append(i)

    def add_item(self, item: Any) -> None:
        self._queue.put(item, block=False)

    def get_item(self) -> Any:
        return self._queue.get()

    def set_item_as_processed(self) -> None:
        self._queue.task_done()

    def wait_queue(self) -> None:
        self._queue.join()
        self._active_threads.clear()
