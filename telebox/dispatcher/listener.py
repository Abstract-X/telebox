from queue import Queue
from abc import ABC, abstractmethod

from telebox.bot.types.update import Update


class AbstractListener(ABC):
    @abstractmethod
    def run(self, updates: Queue[Update]) -> None:
        pass

    @abstractmethod
    def stop(self) -> None:
        pass
