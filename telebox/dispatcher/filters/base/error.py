from abc import ABC, abstractmethod

from telebox.dispatcher.filters.base.base import AbstractFilter


class AbstractErrorFilter(AbstractFilter, ABC):

    @abstractmethod
    def check(self, error, event) -> bool:
        pass
