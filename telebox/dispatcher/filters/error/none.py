from telebox.dispatcher.filters.error_filter import AbstractErrorFilter
from telebox.dispatcher.dispatcher import Event
from telebox.dispatcher.enums.event_type import EventType


class ErrorNoneFilter(AbstractErrorFilter):

    def get_value(self, error: Exception, event: Event, event_type: EventType) -> bool:
        return True

    def check_value(self, value: bool) -> bool:
        return value
