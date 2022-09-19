from telebox.dispatcher.filters.base.event import AbstractEventFilter
from telebox.telegram_bot.types.types.message import Message


class CommandFilter(AbstractEventFilter):

    def __init__(self, command: str, username: str, *, ignore_case: bool = True):
        if not command.startswith("/"):
            command = f"/{command}"

        command = command.lower() if ignore_case else command
        self._ignore_case = ignore_case
        self._variants = {command, f"{command}@{username.lower()}"}

    def check_event(self, event: Message) -> bool:
        command_text = event.text.split(" ", 1)[0]

        if self._ignore_case:
            command_text = command_text.lower()

        return command_text in self._variants
