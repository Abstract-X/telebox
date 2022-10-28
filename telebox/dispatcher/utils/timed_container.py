from typing import Any
import time


class TimedContainer:

    def __init__(self, initial_item: Any):
        self.items = [initial_item]
        self.time = time.monotonic()

    def add(self, item: Any) -> None:
        self.items.append(item)
        self.time = time.monotonic()
