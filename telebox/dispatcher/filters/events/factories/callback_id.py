from typing import Any, Iterable

from telebox.dispatcher.filters.events.factory import AbstractEventFilterFactory
from telebox.dispatcher.filters.events.filter import AbstractEventFilter
from telebox.dispatcher.filters.events.cache import AbstractEventFilterCache
from telebox.dispatcher.enums.event_type import EventType
from telebox.bot.types.types.callback_query import CallbackQuery
from telebox.utils.callback_data import get_parsed_callback_data


class CallbackIDFilterCache(AbstractEventFilterCache):

    def create(self, event: CallbackQuery) -> Any:
        if event.data is not None:
            id_, _ = get_parsed_callback_data(event.data)

            return id_


class CallbackIDFilter(AbstractEventFilter):

    def __init__(self, ids: Iterable[Any], cache: CallbackIDFilterCache):
        if not ids:
            raise ValueError("No ids!")

        self._ids = set(ids)
        self._cache = cache

    def get_event_types(self) -> set[EventType]:
        return {EventType.CALLBACK_QUERY}

    def check_event(self, event: CallbackQuery) -> bool:
        return self._cache.get(event) in self._ids


class CallbackIDFilterFactory(AbstractEventFilterFactory):

    def __init__(self):
        self._cache = CallbackIDFilterCache()

    def get(self, *ids: Any) -> CallbackIDFilter:
        return CallbackIDFilter(ids, self._cache)
