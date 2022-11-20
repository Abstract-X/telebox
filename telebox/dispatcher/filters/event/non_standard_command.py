from typing import Optional, Union

from telebox.dispatcher.filters.event_filter import AbstractEventFilter
from telebox.dispatcher.enums.event_type import EventType
from telebox.dispatcher.utils.media_group import MediaGroup
from telebox.bot.types.types.message import Message


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

    def get_event_types(self) -> set[EventType]:
        return {
            EventType.MESSAGE,
            EventType.EDITED_MESSAGE,
            EventType.CHANNEL_POST,
            EventType.EDITED_CHANNEL_POST,
            EventType.MEDIA_GROUP
        }

    def get_value(self, event: Union[Message, MediaGroup]) -> Optional[str]:
        if isinstance(event, MediaGroup):
            for i in event:
                command = _get_command(i)

                if command is not None:
                    return command

        return _get_command(event)

    def check_value(self, value: Optional[str]) -> bool:
        if (value is not None) and value.startswith(self._prefix):
            if not self._commands:
                return True

            if self._ignore_case:
                value = value.lower()

            return value in self._commands

        return False


def _get_command(message: Message) -> Optional[str]:
    text = message.get_text()

    if text is not None:
        return text.split(" ", 1)[0]
