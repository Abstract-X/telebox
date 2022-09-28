from collections import deque
from typing import TypeVar, Callable
from threading import Lock
import time


Value = TypeVar("Value")
_DELAY_SECS = 0.05


class DoubleEndedQueue:

    def __init__(self):
        self._deque = deque()
        self._not_processed_items = 0
        self._notification_lock = Lock()
        self._getting_lock = Lock()

    def add_on_left(self, value: Value) -> None:
        self._deque.appendleft(value)

    def add_on_right(self, value: Value) -> None:
        self._deque.append(value)

    def get_on_left(self) -> Value:
        return self._get(self._deque.popleft)

    def get_on_right(self) -> Value:
        return self._get(self._deque.pop)

    def notify(self) -> None:
        with self._notification_lock:
            self._not_processed_items -= 1

    def wait_processing(self) -> None:
        while self._not_processed_items:
            time.sleep(_DELAY_SECS)

    def _get(self, getter: Callable) -> Value:
        with self._getting_lock:
            while True:
                if self._deque:
                    self._not_processed_items += 1

                    return getter()

                time.sleep(_DELAY_SECS)
