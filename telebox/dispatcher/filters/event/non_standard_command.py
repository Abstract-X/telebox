from telebox.dispatcher.filters.event_filter import AbstractEventFilter
from telebox.dispatcher.dispatcher import Event
from telebox.dispatcher.enums.event_type import EventType
from telebox.telegram_bot.types.types.message import Message


class NonStandardCommandFilter(AbstractEventFilter):

    def __init__(self, *commands: str, prefix: str, ignore_case: bool = True):
        if not commands:
            raise ValueError("No commands!")

        self._commands = set()

        for i in commands:
            if not i.startswith(prefix):
                i = f"{prefix}{i}"

            if ignore_case:
                i = i.lower()

            self._commands.add(i)

        self._prefix = prefix
        self._ignore_case = ignore_case

    def get_value(self, event: Event, event_type: EventType) -> set[str]:
        commands = set()

        if isinstance(event, Message):
            text = event.get_text()

            if text is not None:
                for i in text.split(" "):
                    if i.startswith(self._prefix):
                        commands.add(i.lower() if self._ignore_case else i)

        return commands

    def check_value(self, value: set[str]) -> bool:
        return any(i in self._commands for i in value)
