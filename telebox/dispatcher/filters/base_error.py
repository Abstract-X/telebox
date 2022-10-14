from abc import ABC, abstractmethod

from telebox.dispatcher.filters.base import AbstractFilter


class AbstractErrorFilter(AbstractFilter, ABC):

    @abstractmethod
    def get_value(self, error, event, event_type):
        pass

    @abstractmethod
    def check_value(self, value) -> bool:
        pass
