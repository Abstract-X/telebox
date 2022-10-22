from typing import Optional

from telebox.dispatcher.filters.event_filter import AbstractEventFilter
from telebox.dispatcher.typing import Event
from telebox.dispatcher.enums.event_type import EventType
from telebox.telegram_bot.types.types.message import Message
from telebox.telegram_bot.consts import message_entity_types


class CommandFilter(AbstractEventFilter):

    def __init__(self, *commands: str, username: str, ignore_case: bool = True):
        self._commands = set()

        for i in commands:
            if not i.startswith("/"):
                i = f"/{i}"

            if ignore_case:
                i = i.lower()

            self._commands.update((i, f"{i}@{username.lower()}"))

        self._ignore_case = ignore_case

    def get_value(self, event: Event, event_type: EventType) -> Optional[str]:
        if isinstance(event, Message):
            for i in event.get_entities():
                if (i.type == message_entity_types.BOT_COMMAND) and (i.offset == 0):
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
