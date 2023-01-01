from contextvars import ContextVar
from abc import ABC, abstractmethod


class AbstractEventFilterCache(ABC):

    def __init_subclass__(cls, **kwargs):
        cls.__current_event_context = ContextVar(f"{cls.__name__}_current_event_context")
        cls.__result_context = ContextVar(f"{cls.__name__}_result_context")

    @abstractmethod
    def create(self, event):
        pass

    def get(self, event):
        try:
            current_event = self.__current_event_context.get()
        except LookupError:
            result = self.create(event)
            self.__current_event_context.set(event)
            self.__result_context.set(result)
        else:
            if current_event is event:
                result = self.__result_context.get()
            else:
                result = self.create(event)
                self.__current_event_context.set(event)
                self.__result_context.set(result)

        return result
