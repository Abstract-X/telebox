from telebox.dispatcher.filters.event_filter import AbstractEventFilter
from telebox.dispatcher.dispatcher import Event
from telebox.dispatcher.enums.event_type import EventType
from telebox.telegram_bot.types.types.message import Message
from telebox.telegram_bot.consts import message_entity_types


class CommandFilter(AbstractEventFilter):

    def __init__(self, *commands: str, username: str, ignore_case: bool = True):
        if not commands:
            raise ValueError("No commands!")

        self._commands = set()

        for i in commands:
            if not i.startswith("/"):
                i = f"/{i}"

            if ignore_case:
                i = i.lower()

            self._commands.update((i, f"{i}@{username.lower()}"))

        self._ignore_case = ignore_case

    def get_value(self, event: Event, event_type: EventType) -> set[str]:
        commands = set()

        if isinstance(event, Message):
            for i in event.get_entities():
                if i.type == message_entity_types.BOT_COMMAND:
                    command = event.get_entity_text(i)

                    if self._ignore_case:
                        command = command.lower() if self._ignore_case else command
                    elif "@" in command:
                        command, username = command.split("@", 1)
                        command = f"{command}@{username.lower()}"

                    commands.add(command)

        return commands

    def check_value(self, value: set[str]) -> bool:
        return any(i in self._commands for i in value)
