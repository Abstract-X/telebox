from typing import Optional, Union, Iterable

from telebox.dispatcher.filters.events.factory import AbstractEventFilterFactory
from telebox.dispatcher.filters.events.filter import AbstractEventFilter
from telebox.dispatcher.filters.events.cache import AbstractEventFilterCache
from telebox.dispatcher.enums.event_type import EventType
from telebox.dispatcher.utils.media_group import MediaGroup
from telebox.bot.types.types.message import Message
from telebox.bot.consts import message_entity_types


class CommandFilterCache(AbstractEventFilterCache):

    def create(self, event: Union[Message, MediaGroup]) -> Optional[str]:
        message = event.messages[0] if isinstance(event, MediaGroup) else event

        for i in message.get_entities():
            if (i.offset == 0) and (i.type == message_entity_types.BOT_COMMAND):
                return message.get_entity_text(i)


class CommandFilter(AbstractEventFilter):

    def __init__(
        self,
        commands: Iterable[str],
        username: str,
        ignore_case: bool,
        cache: CommandFilterCache
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
        self._cache = cache

    def get_event_types(self) -> set[EventType]:
        return {
            EventType.MESSAGE,
            EventType.EDITED_MESSAGE,
            EventType.MEDIA_GROUP
        }

    def check_event(self, event: Union[Message, MediaGroup]) -> bool:
        command = self._cache.get(event)

        if command is not None:
            if not self._commands:
                return True

            if self._ignore_case:
                command = command.lower()
            elif "@" in command:
                command, username = command.split("@", 1)
                command = f"{command}@{username.lower()}"

            return command in self._commands

        return False


class CommandFilterFactory(AbstractEventFilterFactory):

    def __init__(self, username: str):
        self._username = username
        self._cache = CommandFilterCache()

    def get_filter(self, *commands: str, ignore_case: bool = True) -> CommandFilter:
        return CommandFilter(commands, self._username, ignore_case, self._cache)
