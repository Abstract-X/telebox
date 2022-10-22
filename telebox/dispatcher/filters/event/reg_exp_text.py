from typing import Pattern, Optional

from telebox.dispatcher.filters.event_filter import AbstractEventFilter
from telebox.dispatcher.typing import Event
from telebox.dispatcher.enums.event_type import EventType
from telebox.telegram_bot.types.types.message import Message


class RegExpTextFilter(AbstractEventFilter):

    def __init__(self, *patterns: Pattern, full_match: bool = True):
        self._patterns = patterns
        self._full_match = full_match

    def get_value(self, event: Event, event_type: EventType) -> Optional[str]:
        if isinstance(event, Message):
            return event.get_text()

    def check_value(self, value: Optional[str]) -> bool:
        if value is not None:
            if not self._patterns:
                return True

            if self._full_match:
                return any(i.fullmatch(value) is not None for i in self._patterns)
            else:
                return any(i.match(value) is not None for i in self._patterns)

        return False
