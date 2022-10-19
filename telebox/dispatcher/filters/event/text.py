from typing import Optional

from telebox.dispatcher.filters.event_filter import AbstractEventFilter
from telebox.dispatcher.dispatcher import Event
from telebox.dispatcher.enums.event_type import EventType
from telebox.telegram_bot.types.types.message import Message


class TextFilter(AbstractEventFilter):

    def __init__(self, *texts: str, ignore_case: bool = False):
        self._texts = {i.lower() for i in texts} if ignore_case else set(texts)
        self._ignore_case = ignore_case

    def get_value(self, event: Event, event_type: EventType) -> Optional[str]:
        if isinstance(event, Message):
            text = event.get_text()

            if text is not None:
                return text.lower() if self._ignore_case else text

    def check_value(self, value: Optional[str]) -> bool:
        return value in self._texts if self._texts else value is not None
