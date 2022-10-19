from typing import Optional, Any

from telebox.dispatcher.filters.event_filter import AbstractEventFilter
from telebox.dispatcher.dispatcher import Event
from telebox.dispatcher.enums.event_type import EventType
from telebox.utils.callback_data_builders.builder import AbstractCallbackDataBuilder
from telebox.telegram_bot.types.types.callback_query import CallbackQuery


class CallbackDataFilter(AbstractEventFilter):

    def __init__(self, *keys: Any, builder: AbstractCallbackDataBuilder):
        if not keys:
            raise ValueError("No keys!")

        self._keys = set(keys)
        self._builder = builder

    def get_value(self, event: Event, event_type: EventType) -> Optional[str]:
        if isinstance(event, CallbackQuery) and (event.data is not None):
            key, _ = self._builder.parse(event.data)

            return key

    def check_value(self, value: Optional[str]) -> bool:
        return value in self._keys
