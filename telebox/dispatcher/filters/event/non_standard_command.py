from typing import Optional

from telebox.dispatcher.filters.event_filter import AbstractEventFilter
from telebox.dispatcher.typing import Event
from telebox.dispatcher.enums.event_type import EventType
from telebox.telegram_bot.types.types.message import Message


class NonStandardCommandFilter(AbstractEventFilter):

    def __init__(self, *commands: str, prefix: str, ignore_case: bool = True):
        self._commands = set()

        for i in commands:
            if not i.startswith(prefix):
                i = f"{prefix}{i}"

            if ignore_case:
                i = i.lower()

            self._commands.add(i)

        self._prefix = prefix
        self._ignore_case = ignore_case

    def get_value(self, event: Event, event_type: EventType) -> Optional[str]:
        if isinstance(event, Message):
            text = event.get_text()

            if text is not None:
                return text.split(" ", 1)[0]

    def check_value(self, value: Optional[str]) -> bool:
        if (value is not None) and value.startswith(self._prefix):
            if not self._commands:
                return True

            if self._ignore_case:
                value = value.lower()

            return value in self._commands

        return False
