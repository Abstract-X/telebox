from contextvars import ContextVar
from abc import ABC, abstractmethod


class AbstractErrorFilterCache(ABC):

    def __init_subclass__(cls, **kwargs):
        cls.__current_error_event_context = ContextVar(
            f"{cls.__name__}_current_error_event_context"
        )
        cls.__value_context = ContextVar(f"{cls.__name__}_value_context")

    @abstractmethod
    def create(self, error, event):
        pass

    def get(self, error, event):
        try:
            current_error, current_event = self.__current_error_event_context.get()
        except LookupError:
            return self._set(error, event)

        if not ((error is current_error) and (event is current_event)):
            return self._set(error, event)

        return self.__value_context.get()

    def _set(self, error, event):
        value = self.create(error, event)
        self.__current_error_event_context.set((error, event))
        self.__value_context.set(value)

        return value
