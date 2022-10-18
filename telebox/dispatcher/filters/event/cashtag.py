from typing import Optional

from telebox.dispatcher.filters.event_filter import AbstractEventFilter
from telebox.dispatcher.dispatcher import Event
from telebox.dispatcher.enums.event_type import EventType
from telebox.telegram_bot.types.types.message import Message


class CashtagFilter(AbstractEventFilter):

    def __init__(self, *cashtags: str, ignore_case: bool = True):
        if not cashtags:
            raise ValueError("No cashtags!")

        self._cashtags = set()

        for i in cashtags:
            if not i.startswith("$"):
                i = f"${i}"

            if ignore_case:
                i = i.lower()

            self._cashtags.add(i)

        self._ignore_case = ignore_case

    def get_value(self, event: Event, event_type: EventType) -> Optional[str]:
        if isinstance(event, Message) and (event.text is not None):
            cashtag = event.text.split(" ", 1)[0]

            return cashtag.lower() if self._ignore_case else cashtag

    def check_value(self, value: Optional[str]) -> bool:
        return value in self._cashtags
