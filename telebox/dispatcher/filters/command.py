from typing import Optional, Union

from telebox.dispatcher.filter import AbstractFilter
from telebox.dispatcher.types.media_group import MediaGroup
from telebox.bot.types.message import Message
from telebox.bot.consts import message_entity_types


class CommandFilter(AbstractFilter):
    def __init__(
        self,
        *commands: str,
        username: Optional[str] = None,
        ignore_case: bool = True
    ):
        self._commands = set()

        for i in commands:
            if not i.startswith("/"):
                i = f"/{i}"

            if ignore_case:
                i = i.lower()

            self._commands.add(i)

            if username:
                self._commands.add(f"{i}@{username.lower()}")

        self._ignore_case = ignore_case

    def get_value(self, event: Union[Message, MediaGroup]) -> Optional[str]:
        for i in event.get_entities():
            if (i.offset == 0) and (i.type == message_entity_types.BOT_COMMAND):
                return event.get_entity_text(i)

    def check_value(self, value: Optional[str]) -> bool:
        if value is not None:
            if not self._commands:
                return True

            if self._ignore_case:
                value = value.lower()
            elif "@" in value:
                command, username = value.split("@", 1)
                value = f"{command}@{username.lower()}"

            return value in self._commands

        return False
