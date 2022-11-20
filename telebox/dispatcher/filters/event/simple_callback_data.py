from typing import Optional

from telebox.dispatcher.filters.event_filter import AbstractEventFilter
from telebox.dispatcher.enums.event_type import EventType
from telebox.bot.types.types.callback_query import CallbackQuery


class SimpleCallbackDataFilter(AbstractEventFilter):

    def __init__(self, *data: str):
        self._data = data

    def get_event_types(self) -> set[EventType]:
        return {EventType.CALLBACK_QUERY}

    def get_value(self, event: CallbackQuery) -> Optional[str]:
        return event.data

    def check_value(self, value: Optional[str]) -> bool:
        return value in self._data if self._data else value is not None
