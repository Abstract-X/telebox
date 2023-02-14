from typing import Pattern, Union, Iterable

from telebox.dispatcher.filters.events.factory import AbstractEventFilterFactory
from telebox.dispatcher.filters.events.filter import AbstractEventFilter
from telebox.dispatcher.filters.events.cache import AbstractEventFilterCache
from telebox.dispatcher.enums.event_type import EventType
from telebox.dispatcher.utils.media_group import MediaGroup
from telebox.bot.types.types.message import Message


class RETextFilterCache(AbstractEventFilterCache):

    def create(self, event: Union[Message, MediaGroup]) -> list[str]:
        texts = []
        messages = event.messages if isinstance(event, MediaGroup) else [event]

        for i in messages:
            text = i.get_text()

            if text is not None:
                texts.append(text)

        return texts


class RETextFilter(AbstractEventFilter):

    def __init__(self, patterns: Iterable[Pattern], full_match: bool, cache: RETextFilterCache):
        if not patterns:
            raise ValueError("No patterns!")

        self._patterns = patterns
        self._full_match = full_match
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
        for text in self._cache.get(event):
            if self._full_match:
                if any(i.fullmatch(text) is not None for i in self._patterns):
                    return True
            else:
                if any(i.match(text) is not None for i in self._patterns):
                    return True

        return False


class RETextFilterFactory(AbstractEventFilterFactory):

    def __init__(self):
        self._cache = RETextFilterCache()

    def get_filter(self, *patterns: Pattern, full_match: bool = False) -> RETextFilter:
        return RETextFilter(patterns, full_match, self._cache)
