from typing import Optional

from telebox.dispatcher.filters.filter import AbstractFilter
from telebox.bot.types.callback_query import CallbackQuery


class CallbackDataFilter(AbstractFilter):
    def __init__(self, *data: str):
        self._data = set(data)

    def get_value(self, event: CallbackQuery) -> Optional[str]:
        return event.data

    def check_value(self, value: Optional[str]) -> bool:
        return value in self._data if self._data else value is not None
