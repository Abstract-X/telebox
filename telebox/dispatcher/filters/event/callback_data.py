from typing import Optional, Any

from telebox.dispatcher.filters.event_filter import AbstractEventFilter
from telebox.telegram_bot.types.types.callback_query import CallbackQuery
from telebox.utils.callback_data_builders.builder import AbstractCallbackDataBuilder


class CallbackDataFilter(AbstractEventFilter):

    def __init__(self, *filter_keys: Any, builder: AbstractCallbackDataBuilder):
        self._filter_keys = set(filter_keys)
        self._builder = builder

    def get_value(self, event: CallbackQuery) -> Optional[str]:
        if event.data is not None:
            filter_key, _ = self._builder.parse(event.data)

            return filter_key

    def check_value(self, value: Optional[str]) -> bool:
        return value in self._filter_keys
