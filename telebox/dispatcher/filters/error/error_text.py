from telebox.dispatcher.filters.base_error import AbstractErrorFilter
from telebox.dispatcher.enums.event_type import EventType
from telebox.typing import Event


class ErrorTextFilter(AbstractErrorFilter):

    def __init__(self, *texts: str, ignore_case: bool = False):
        self._texts = {i.lower() for i in texts} if ignore_case else set(texts)
        self._ignore_case = ignore_case

    def get_value(self, error: Exception, event: Event, event_type: EventType) -> str:
        return str(error).lower() if self._ignore_case else str(error)

    def check_value(self, value: Exception) -> bool:
        return value in self._texts
