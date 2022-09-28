from abc import ABC, abstractmethod

from telebox.dispatcher.handlers.base import AbstractHandler


class AbstractEventHandler(AbstractHandler, ABC):

    @abstractmethod
    def process(self, event) -> None:
        pass
