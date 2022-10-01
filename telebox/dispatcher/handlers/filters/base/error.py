from abc import ABC, abstractmethod

from telebox.dispatcher.handlers.filters.base.base import AbstractFilter


class AbstractErrorFilter(AbstractFilter, ABC):

    @abstractmethod
    def get_value(self, error, event):
        pass

    @abstractmethod
    def check_value(self, value) -> bool:
        pass
