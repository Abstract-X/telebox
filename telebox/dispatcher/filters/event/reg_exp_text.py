from typing import Pattern

from telebox.dispatcher.filters.base.event import AbstractEventFilter
from telebox.telegram_bot.types.types.message import Message


class RegExpTextFilter(AbstractEventFilter):

    def __init__(self, text: Pattern):
        self._text = text

    def check_event(self, event: Message) -> bool:
        return self._text.fullmatch(event.text) is not None
