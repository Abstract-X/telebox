from typing import Optional, Union

from telebox.dispatcher.filters.filter import AbstractFilter
from telebox.dispatcher.types.media_group import MediaGroup
from telebox.bot.types.message import Message


class TextCommandFilter(AbstractFilter):
    def __init__(
        self,
        *commands: str,
        prefix: Optional[str] = None,
        ignore_case: bool = True
    ):
        self._commands = set()

        for i in commands:
            if not i.startswith(prefix):
                i = f"{prefix}{i}"

            if ignore_case:
                i = i.lower()

            self._commands.add(i)

        self._prefix = prefix or ""
        self._ignore_case = ignore_case

    def get_value(self, event: Union[Message, MediaGroup]) -> Optional[str]:
        message = event.messages[0] if isinstance(event, MediaGroup) else event
        text = message.get_text()

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
