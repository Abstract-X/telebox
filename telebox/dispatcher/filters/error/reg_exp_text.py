from typing import Pattern

from telebox.dispatcher.filters.error_filter import AbstractErrorFilter
from telebox.dispatcher.dispatcher import Event
from telebox.dispatcher.enums.event_type import EventType


class ErrorRegExpTextFilter(AbstractErrorFilter):

    def __init__(self, *patterns: Pattern, full_match: bool = True):
        if not patterns:
            raise ValueError("No patterns!")

        self._patterns = set(patterns)
        self._full_match = full_match

    def get_value(self, error: Exception, event: Event, event_type: EventType) -> str:
        return str(error)

    def check_value(self, value: str) -> bool:
        if self._full_match:
            return any(i.fullmatch(value) is not None for i in self._patterns)
        else:
            return any(i.match(value) is not None for i in self._patterns)
