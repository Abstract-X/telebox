from abc import ABC, abstractmethod

from telebox.dispatcher.filters.base import AbstractFilter


class AbstractEventFilter(AbstractFilter, ABC):

    @abstractmethod
    def get_value(self, event):
        pass

    @abstractmethod
    def check_value(self, value) -> bool:
        pass
