from typing import Optional, Any

from telebox.dispatcher.filters.event_filter import AbstractEventFilter
from telebox.dispatcher.enums.event_type import EventType
from telebox.utils.callback_data_builders.builder import AbstractCallbackDataBuilder
from telebox.bot.types.types.callback_query import CallbackQuery


class CallbackDataFilter(AbstractEventFilter):

    def __init__(self, *keys: Any, builder: AbstractCallbackDataBuilder):
        self._keys = set(keys)
        self._builder = builder

    def get_event_types(self) -> set[EventType]:
        return {EventType.CALLBACK_QUERY}

    def get_value(self, event: CallbackQuery) -> Optional[str]:
        if event.data is not None:
            key, _ = self._builder.get_parsed_data(event.data)

            return key

    def check_value(self, value: Optional[str]) -> bool:
        return value in self._keys if self._keys else value is not None
