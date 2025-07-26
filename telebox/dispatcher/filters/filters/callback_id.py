from typing import Optional

from telebox.dispatcher.filters.filter import AbstractFilter
from telebox.dispatcher.enums.event_type import EventType
from telebox.bot.types.types.callback_query import CallbackQuery
from telebox.utils.callback_data import get_parsed_callback_data


class CallbackIDFilter(AbstractFilter):

    def __init__(self, *ids: int):
        if not ids:
            raise ValueError("No ids!")

        self._ids = set(ids)

    def get_event_types(self) -> set[EventType]:
        return {EventType.CALLBACK_QUERY}

    def get_value(self, event: CallbackQuery) -> Optional[int]:
        if event.data is not None:
            id_, _ = get_parsed_callback_data(event.data)

            return id_

    def check_value(self, value: Optional[int]) -> bool:
        return value in self._ids
