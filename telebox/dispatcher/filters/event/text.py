from typing import Optional

from telebox.dispatcher.filters.event_filter import AbstractEventFilter
from telebox.dispatcher.typing import Event
from telebox.dispatcher.enums.event_type import EventType
from telebox.telegram_bot.types.types.message import Message


class TextFilter(AbstractEventFilter):

    def __init__(self, *texts: str, full_match: bool = True, ignore_case: bool = False):
        self._texts = {i.lower() for i in texts} if ignore_case else set(texts)
        self._full_match = full_match
        self._ignore_case = ignore_case

    def get_value(self, event: Event, event_type: EventType) -> Optional[str]:
        if isinstance(event, Message):
            return event.get_text()

    def check_value(self, value: Optional[str]) -> bool:
        if value is not None:
            if not self._texts:
                return True

            if self._ignore_case:
                value = value.lower()

            if self._full_match:
                return value in self._texts
            else:
                return any(i in value for i in self._texts)

        return False
