from typing import Optional, Union

from telebox.dispatcher.filters.factory import AbstractFilterFactory
from telebox.dispatcher.filters.filter import AbstractFilter
from telebox.dispatcher.enums.event_type import EventType
from telebox.dispatcher.utils.media_group import MediaGroup
from telebox.bot.types.message import Message
from telebox.bot.consts import message_entity_types


class CommandFilter(AbstractFilter):

    def __init__(
        self,
        *commands: str,
        username: str,
        ignore_case: bool
    ):
        self._commands = set()
        username = username.lower()

        for i in commands:
            if not i.startswith("/"):
                i = f"/{i}"

            if ignore_case:
                i = i.lower()

            self._commands.update((i, f"{i}@{username}"))

        self._ignore_case = ignore_case

    def get_event_types(self) -> set[EventType]:
        return {
            EventType.MESSAGE,
            EventType.EDITED_MESSAGE,
            EventType.MEDIA_GROUP
        }

    def get_value(self, event: Union[Message, MediaGroup]) -> Optional[str]:
        message = event.messages[0] if isinstance(event, MediaGroup) else event

        for i in message.get_entities():
            if (i.offset == 0) and (i.type == message_entity_types.BOT_COMMAND):
                return message.get_entity_text(i)

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


class CommandFilterFactory(AbstractFilterFactory):

    def __init__(self, username: str):
        self._username = username

    def get(self, *commands: str, ignore_case: bool = True) -> CommandFilter:
        return CommandFilter(
            *commands,
            username=self._username,
            ignore_case=ignore_case
        )
