from abc import ABC, abstractmethod

from telebox.dispatcher.handlers.handler import AbstractHandler


class AbstractEventHandler(AbstractHandler, ABC):

    @abstractmethod
    def process(self, event) -> None:
        pass
