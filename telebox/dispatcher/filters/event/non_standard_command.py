from typing import Optional

from telebox.dispatcher.filters.event_filter import AbstractEventFilter
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

        self._ignore_case = ignore_case

    def get_value(self, event: Message) -> Optional[str]:
        if event.text is not None:
            command_text = event.text.split(" ", 1)[0]

            if self._ignore_case:
                command_text = command_text.lower()

            return command_text

    def check_value(self, value: Optional[str]) -> bool:
        return value in self._commands
