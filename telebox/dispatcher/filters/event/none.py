from telebox.dispatcher.filters.event_filter import AbstractEventFilter
from telebox.dispatcher.dispatcher import Event
from telebox.dispatcher.enums.event_type import EventType


class NoneFilter(AbstractEventFilter):

    def get_value(self, event: Event, event_type: EventType) -> bool:
        return True

    def check_value(self, value: bool) -> bool:
        return value
