from typing import Union, Iterable

from telebox.dispatcher.filters.events.factory import AbstractEventFilterFactory
from telebox.dispatcher.filters.events.filter import AbstractEventFilter
from telebox.dispatcher.filters.events.cache import AbstractEventFilterCache
from telebox.dispatcher.enums.event_type import EventType
from telebox.dispatcher.utils.media_group import MediaGroup
from telebox.bot.types.types.message import Message
from telebox.bot.consts import message_entity_types


class CashtagFilterCache(AbstractEventFilterCache):

    def create(self, event: Union[Message, MediaGroup]) -> set[str]:
        cashtags = set()
        messages = event.messages if isinstance(event, MediaGroup) else [event]

        for message in messages:
            for entity in message.get_entities():
                if entity.type == message_entity_types.CASHTAG:
                    cashtags.add(
                        message.get_entity_text(entity)
                    )

        return cashtags


class CashtagFilter(AbstractEventFilter):

    def __init__(self, cashtags: Iterable[str], cache: CashtagFilterCache):
        self._cashtags = set()

        for i in cashtags:
            if not i.startswith("$"):
                i = f"${i}"

            self._cashtags.add(i.upper())

        self._cache = cache

    def get_event_types(self) -> set[EventType]:
        return {
            EventType.MESSAGE,
            EventType.EDITED_MESSAGE,
            EventType.CHANNEL_POST,
            EventType.EDITED_CHANNEL_POST,
            EventType.MEDIA_GROUP,
            EventType.CHANNEL_MEDIA_GROUP
        }

    def check_event(self, event: Union[Message, MediaGroup]) -> bool:
        cashtags = self._cache.get(event)

        if self._cashtags:
            return any(i in self._cashtags for i in cashtags)

        return bool(cashtags)


class CashtagFilterFactory(AbstractEventFilterFactory):

    def __init__(self):
        self._cache = CashtagFilterCache()

    def get_filter(self, *cashtags: str) -> CashtagFilter:
        return CashtagFilter(cashtags, self._cache)
