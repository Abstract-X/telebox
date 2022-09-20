from abc import ABC, abstractmethod

from telebox.dispatcher.filters.base.base import AbstractFilter


class AbstractEventFilter(AbstractFilter, ABC):

    @abstractmethod
    def check(self, event) -> bool:
        pass
