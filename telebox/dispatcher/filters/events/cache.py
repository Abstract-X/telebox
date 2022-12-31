from contextvars import ContextVar
from abc import ABC, abstractmethod


class AbstractEventFilterCache(ABC):

    def __init_subclass__(cls, **kwargs):
        cls.__context = ContextVar(f"{cls.__name__}_context")

    @abstractmethod
    def create(self, event):
        pass

    def get(self, event):
        try:
            value = self.__context.get()
        except LookupError:
            value = self.create(event)
            self.__context.set(value)

        return value
