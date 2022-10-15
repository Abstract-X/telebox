from abc import ABC, abstractmethod

from telebox.dispatcher.handlers.handler import AbstractHandler


class AbstractErrorHandler(AbstractHandler, ABC):

    @abstractmethod
    def process(self, error, event, event_type):
        pass
