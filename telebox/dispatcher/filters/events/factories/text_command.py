from typing import Optional, Union, Iterable

from telebox.dispatcher.filters.events.factory import AbstractEventFilterFactory
from telebox.dispatcher.filters.events.filter import AbstractEventFilter
from telebox.dispatcher.filters.events.cache import AbstractEventFilterCache
from telebox.dispatcher.enums.event_type import EventType
from telebox.dispatcher.utils.media_group import MediaGroup
from telebox.bot.types.types.message import Message


class TextCommandFilterCache(AbstractEventFilterCache):

    def create(self, event: Union[Message, MediaGroup]) -> Optional[str]:
        message = event.messages[0] if isinstance(event, MediaGroup) else event
        text = message.get_text()

        if text is not None:
            return text.split(" ", 1)[0]


class TextCommandFilter(AbstractEventFilter):

    def __init__(
        self,
        commands: Iterable[str],
        prefix: str,
        ignore_case: bool,
        cache: TextCommandFilterCache
    ):
        self._commands = set()

        for i in commands:
            if not i.startswith(prefix):
                i = f"{prefix}{i}"

            if ignore_case:
                i = i.lower()

            self._commands.add(i)

        self._prefix = prefix
        self._ignore_case = ignore_case
        self._cache = cache

    def get_event_types(self) -> set[EventType]:
        return {
            EventType.MESSAGE,
            EventType.EDITED_MESSAGE,
            EventType.CHANNEL_POST,
            EventType.EDITED_CHANNEL_POST,
            EventType.MEDIA_GROUP,
            EventType.CHANNEL_MEDIA_GROUP
        }

    def check_event(self, event: Union[Message, MediaGroup]) -> bool:
        command = self._cache.get(event)

        if (command is not None) and command.startswith(self._prefix):
            if not self._commands:
                return True

            if self._ignore_case:
                command = command.lower()

            return command in self._commands

        return False


class TextCommandFilterFactory(AbstractEventFilterFactory):

    def __init__(self, prefix: str = ""):
        self._prefix = prefix
        self._cache = TextCommandFilterCache()

    def get_filter(self, *commands: str, ignore_case: bool = True) -> TextCommandFilter:
        return TextCommandFilter(commands, self._prefix, ignore_case, self._cache)
