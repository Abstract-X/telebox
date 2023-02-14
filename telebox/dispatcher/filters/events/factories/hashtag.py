from typing import Union, Iterable

from telebox.dispatcher.filters.events.factory import AbstractEventFilterFactory
from telebox.dispatcher.filters.events.filter import AbstractEventFilter
from telebox.dispatcher.filters.events.cache import AbstractEventFilterCache
from telebox.dispatcher.enums.event_type import EventType
from telebox.dispatcher.utils.media_group import MediaGroup
from telebox.bot.types.types.message import Message
from telebox.bot.consts import message_entity_types


class HashtagFilterCache(AbstractEventFilterCache):

    def create(self, event: Union[Message, MediaGroup]) -> set[str]:
        hashtags = set()
        messages = event.messages if isinstance(event, MediaGroup) else [event]

        for message in messages:
            for entity in message.get_entities():
                if entity.type == message_entity_types.HASHTAG:
                    hashtags.add(
                        message.get_entity_text(entity)
                    )

        return hashtags


class HashtagFilter(AbstractEventFilter):

    def __init__(self, hashtags: Iterable[str], ignore_case: bool, cache: HashtagFilterCache):
        self._hashtags = set()

        for i in hashtags:
            if not i.startswith("#"):
                i = f"#{i}"

            if ignore_case:
                i = i.lower()

            self._hashtags.add(i)

        self._ignore_case = ignore_case
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
        hashtags = self._cache.get(event)

        if not self._hashtags:
            return bool(hashtags)

        for i in hashtags:
            if self._ignore_case:
                i = i.lower()

            if i in self._hashtags:
                return True

        return False


class HashtagFilterFactory(AbstractEventFilterFactory):

    def __init__(self):
        self._cache = HashtagFilterCache()

    def get_filter(self, *hashtags: str, ignore_case: bool = True) -> HashtagFilter:
        return HashtagFilter(hashtags, ignore_case, self._cache)
