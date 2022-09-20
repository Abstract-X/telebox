from typing import Pattern

from telebox.dispatcher.filters.base.event import AbstractEventFilter
from telebox.telegram_bot.types.types.message import Message


class RegExpTextFilter(AbstractEventFilter):

    def __init__(self, *texts: Pattern):
        self._texts = set(texts)

    def check_event(self, event: Message) -> bool:
        for i in self._texts:
            if i.fullmatch(event.text) is not None:
                return True

        return False