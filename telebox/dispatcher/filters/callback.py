from typing import Optional

from telebox.dispatcher.filter import AbstractFilter
from telebox.bot.types.callback_query import CallbackQuery
from telebox.callback_data import get_parsed_callback_data


class CallbackFilter(AbstractFilter):
    def __init__(self, *ids: int):
        if not ids:
            raise ValueError("No ids!")

        self._ids = set(ids)

    def get_value(self, event: CallbackQuery) -> Optional[int]:
        if event.data is not None:
            id_, _ = get_parsed_callback_data(event.data)

            return id_

    def check_value(self, value: Optional[int]) -> bool:
        return value in self._ids
