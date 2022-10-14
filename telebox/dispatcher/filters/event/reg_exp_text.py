from typing import Pattern, Optional

from telebox.dispatcher.filters.base_event import AbstractEventFilter
from telebox.telegram_bot.types.types.message import Message


class RegExpTextFilter(AbstractEventFilter):

    def __init__(self, *texts: Pattern):
        self._texts = set(texts)

    def get_value(self, event: Message) -> Optional[str]:
        return event.text

    def check_value(self, value: Optional[str]) -> bool:
        return (value is not None) and any(i.fullmatch(value) is not None for i in self._texts)
