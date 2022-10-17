from typing import Optional, Any

from telebox.dispatcher.filters.event_filter import AbstractEventFilter
from telebox.dispatcher.enums.event_type import EventType
from telebox.utils.callback_data_builders.builder import AbstractCallbackDataBuilder
from telebox.telegram_bot.types.types.callback_query import CallbackQuery
from telebox.typing import Event


class CallbackDataFilter(AbstractEventFilter):

    def __init__(self, *filter_keys: Any, builder: AbstractCallbackDataBuilder):
        if not filter_keys:
            raise ValueError("No filter keys!")

        self._filter_keys = set(filter_keys)
        self._builder = builder

    def get_value(self, event: Event, event_type: EventType) -> Optional[str]:
        if isinstance(event, CallbackQuery) and (event.data is not None):
            filter_key, _ = self._builder.parse(event.data)

            return filter_key

    def check_value(self, value: Optional[str]) -> bool:
        return value in self._filter_keys
