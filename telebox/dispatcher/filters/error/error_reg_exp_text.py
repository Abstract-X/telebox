from typing import Pattern

from telebox.dispatcher.filters.base_error import AbstractErrorFilter
from telebox.dispatcher.enums.event_type import EventType
from telebox.typing import Event


class ErrorRegExpTextFilter(AbstractErrorFilter):

    def __init__(self, *texts: Pattern):
        self._texts = set(texts)

    def get_value(self, error: Exception, event: Event, event_type: EventType) -> str:
        return str(error)

    def check_value(self, value: str) -> bool:
        return any(i.fullmatch(value) is not None for i in self._texts)
