from telebox.dispatcher.handlers.filters.base.event import AbstractEventFilter
from telebox.telegram_bot.types.types.message import Message


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

    def get_value(self, event: Message) -> str:
        command_text = event.text.split(" ", 1)[0]

        if self._ignore_case:
            command_text = command_text.lower()

        return command_text

    def check_value(self, value: str) -> bool:
        return value in self._commands