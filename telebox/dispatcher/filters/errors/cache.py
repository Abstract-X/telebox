from contextvars import ContextVar
from abc import ABC, abstractmethod


class AbstractErrorFilterCache(ABC):

    def __init_subclass__(cls, **kwargs):
        cls.__current_error_event_context = ContextVar(
            f"{cls.__name__}_current_error_event_context"
        )
        cls.__result_context = ContextVar(f"{cls.__name__}_result_context")

    @abstractmethod
    def create(self, error, event):
        pass

    def get(self, error, event):
        try:
            current_error, current_event = self.__current_error_event_context.get()
        except LookupError:
            result = self.create(error, event)
            self.__current_error_event_context.set((error, event))
            self.__result_context.set(result)
        else:
            if (current_error is error) and (current_event is event):
                result = self.__result_context.get()
            else:
                result = self.create(error, event)
                self.__current_error_event_context.set((error, event))
                self.__result_context.set(result)

        return result
