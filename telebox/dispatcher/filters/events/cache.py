from contextvars import ContextVar
from abc import ABC, abstractmethod


class AbstractEventFilterCache(ABC):

    def __init_subclass__(cls, **kwargs):
        cls.__current_event_context = ContextVar(f"{cls.__name__}_current_event_context")
        cls.__value_context = ContextVar(f"{cls.__name__}_value_context")

    @abstractmethod
    def create(self, event):
        pass

    def get(self, event):
        try:
            current_event = self.__current_event_context.get()
        except LookupError:
            return self._set(event)

        if event is not current_event:
            return self._set(event)

        return self.__value_context.get()

    def _set(self, event):
        value = self.create(event)
        self.__current_event_context.set(event)
        self.__value_context.set(value)

        return value
