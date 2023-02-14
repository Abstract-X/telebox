from typing import Union, Iterable

from telebox.dispatcher.filters.events.factory import AbstractEventFilterFactory
from telebox.dispatcher.filters.events.filter import AbstractEventFilter
from telebox.dispatcher.filters.events.cache import AbstractEventFilterCache
from telebox.dispatcher.enums.event_type import EventType
from telebox.dispatcher.utils.media_group import MediaGroup
from telebox.bot.types.types.message import Message
from telebox.bot.consts import message_entity_types


class TextMentionFilterCache(AbstractEventFilterCache):

    def create(self, event: Union[Message, MediaGroup]) -> set[str]:
        mentions = set()
        messages = event.messages if isinstance(event, MediaGroup) else [event]

        for message in messages:
            for entity in message.get_entities():
                if entity.type == message_entity_types.TEXT_MENTION:
                    mentions.add(
                        message.get_entity_text(entity).lower()
                    )

        return mentions


class TextMentionFilter(AbstractEventFilter):

    def __init__(self, mentions: Iterable[str], cache: TextMentionFilterCache):
        self._mentions = {i.lower() for i in mentions}
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
        mentions = self._cache.get(event)

        if self._mentions:
            return any(i in self._mentions for i in mentions)

        return bool(mentions)


class TextMentionFilterFactory(AbstractEventFilterFactory):

    def __init__(self):
        self._cache = TextMentionFilterCache()

    def get_filter(self, *mentions: str) -> TextMentionFilter:
        return TextMentionFilter(mentions, self._cache)
