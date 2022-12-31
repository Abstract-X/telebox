from typing import Any, Iterable

from telebox.dispatcher.filters.events.factory import AbstractEventFilterFactory
from telebox.dispatcher.filters.events.filter import AbstractEventFilter
from telebox.dispatcher.filters.events.cache import AbstractEventFilterCache
from telebox.dispatcher.enums.event_type import EventType
from telebox.utils.callback_data_builders.builder import AbstractCallbackDataBuilder
from telebox.bot.types.types.callback_query import CallbackQuery


class CallbackKeyFilterCache(AbstractEventFilterCache):

    def __init__(self, builder: AbstractCallbackDataBuilder):
        self._builder = builder

    def create(self, event: CallbackQuery) -> Any:
        if event.data is not None:
            return self._builder.get_key(event.data)


class CallbackKeyFilter(AbstractEventFilter):

    def __init__(self, keys: Iterable[Any], cache: CallbackKeyFilterCache):
        self._keys = set(keys)
        self._cache = cache

    def get_event_types(self) -> set[EventType]:
        return {EventType.CALLBACK_QUERY}

    def check_event(self, event: CallbackQuery) -> bool:
        key = self._cache.get(event)

        if self._keys:
            return key in self._keys

        return key is not None


class CallbackKeyFilterFactory(AbstractEventFilterFactory):

    def __init__(self, builder: AbstractCallbackDataBuilder):
        self._cache = CallbackKeyFilterCache(builder)

    def get_filter(self, *keys: Any) -> CallbackKeyFilter:
        return CallbackKeyFilter(keys, self._cache)
