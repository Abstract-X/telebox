import time
from queue import Queue
from typing import Optional
from threading import Lock
from dataclasses import dataclass

from telebox.dispatcher.double_ended_queue import DoubleEndedQueue
from telebox.dispatcher.enums.event_type import EventType
from telebox.typing import Event


_DELAY_SECS = 0.05


@dataclass(frozen=True)
class Item:
    event: Event
    event_type: EventType
    chat_id: Optional[int] = None


class EventQueue:

    def __init__(self):
        self._queue = DoubleEndedQueue()
        self._delayed_queue = Queue()
        self._delayed_chat_ids: set[int] = set()
        self._notification_lock = Lock()

    def add_item(self, item: Item) -> None:
        if item.chat_id is not None:
            if item.chat_id in self._delayed_chat_ids:
                self._delayed_queue.put(item, block=False)
            else:
                self._delayed_chat_ids.add(item.chat_id)
                self._queue.add_on_left(item)
        else:
            self._queue.add_on_left(item)

    def get_item(self) -> Item:
        return self._queue.get_on_right()

    def notify_about_processed_item(self, item: Item) -> None:
        with self._notification_lock:
            self._delayed_chat_ids.discard(item.chat_id)

        self._queue.notify()

    def wait_processing(self) -> None:
        self._delayed_queue.join()
        self._queue.wait_processing()

    def run_delayed_event_processing(self) -> None:
        remaining_items = set()

        while True:
            item = self._delayed_queue.get()

            try:
                if item in remaining_items:
                    remaining_items.clear()
                    time.sleep(_DELAY_SECS)

                if item.chat_id not in self._delayed_chat_ids:
                    self._delayed_chat_ids.add(item.chat_id)
                    self._queue.add_on_right(item)
                else:
                    self._delayed_queue.put(item, block=False)
                    remaining_items.add(item)
            finally:
                self._delayed_queue.task_done()
