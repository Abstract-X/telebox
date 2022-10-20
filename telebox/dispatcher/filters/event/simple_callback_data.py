from typing import Optional

from telebox.dispatcher.filters.event_filter import AbstractEventFilter
from telebox.dispatcher.dispatcher import Event
from telebox.dispatcher.enums.event_type import EventType
from telebox.telegram_bot.types.types.callback_query import CallbackQuery


class SimpleCallbackDataFilter(AbstractEventFilter):

    def __init__(self, *data: str):
        self._data = data

    def get_value(self, event: Event, event_type: EventType) -> Optional[str]:
        if isinstance(event, CallbackQuery):
            return event.data

    def check_value(self, value: Optional[str]) -> bool:
        return value in self._data if self._data else value is not None
