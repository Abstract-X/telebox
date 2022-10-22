from typing import Type

from telebox.dispatcher.filters.error_filter import AbstractErrorFilter
from telebox.dispatcher.typing import Event
from telebox.dispatcher.enums.event_type import EventType


class ErrorTypeFilter(AbstractErrorFilter):

    def __init__(self, *types: Type[Exception], strictly: bool = False):
        if not types:
            raise ValueError("No types!")

        self._types = types
        self._strictly = strictly

    def get_value(self, error: Exception, event: Event, event_type: EventType) -> Exception:
        return error

    def check_value(self, value: Exception) -> bool:
        return type(value) in self._types if self._strictly else isinstance(value, self._types)
