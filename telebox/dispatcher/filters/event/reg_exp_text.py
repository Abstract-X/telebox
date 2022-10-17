from typing import Pattern, Optional

from telebox.dispatcher.filters.event_filter import AbstractEventFilter
from telebox.dispatcher.dispatcher import Event
from telebox.dispatcher.enums.event_type import EventType
from telebox.telegram_bot.types.types.message import Message


class RegExpTextFilter(AbstractEventFilter):

    def __init__(self, *texts: Pattern):
        self._texts = texts

    def get_value(self, event: Event, event_type: EventType) -> Optional[str]:
        if isinstance(event, Message):
            return event.text

    def check_value(self, value: Optional[str]) -> bool:
        return (value is not None) and any(i.fullmatch(value) is not None for i in self._texts)
