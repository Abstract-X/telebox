from typing import Pattern

from telebox.dispatcher.handlers.filters.base.event import AbstractEventFilter
from telebox.telegram_bot.types.types.message import Message


class RegExpTextFilter(AbstractEventFilter):

    def __init__(self, *texts: Pattern):
        self._texts = set(texts)

    def get_value(self, event: Message) -> str:
        return event.text

    def check_value(self, value: str) -> bool:
        return any(i.fullmatch(value) is not None for i in self._texts)
