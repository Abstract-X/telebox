from contextvars import ContextVar
from abc import ABC, abstractmethod


class AbstractErrorFilterCache(ABC):

    def __init_subclass__(cls, **kwargs):
        cls.__context = ContextVar(f"{cls.__name__}_context")

    @abstractmethod
    def create(self, error, event):
        pass

    def get(self, error, event):
        try:
            value = self.__context.get()
        except LookupError:
            value = self.create(error, event)
            self.__context.set(value)

        return value
