from abc import ABC, abstractmethod

from telebox.dispatcher.handlers.handlers.base import AbstractHandler


class AbstractErrorHandler(AbstractHandler, ABC):

    @abstractmethod
    def process(self, error, event):
        pass
