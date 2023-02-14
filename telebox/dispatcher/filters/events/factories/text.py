from typing import Union, Iterable

from telebox.dispatcher.filters.events.factory import AbstractEventFilterFactory
from telebox.dispatcher.filters.events.filter import AbstractEventFilter
from telebox.dispatcher.filters.events.cache import AbstractEventFilterCache
from telebox.dispatcher.enums.event_type import EventType
from telebox.dispatcher.utils.media_group import MediaGroup
from telebox.bot.types.types.message import Message


class TextFilterCache(AbstractEventFilterCache):

    def create(self, event: Union[Message, MediaGroup]) -> list[str]:
        texts = []
        messages = event.messages if isinstance(event, MediaGroup) else [event]

        for i in messages:
            text = i.get_text()

            if text is not None:
                texts.append(text)

        return texts


class TextFilter(AbstractEventFilter):

    def __init__(
        self,
        texts: Iterable[str],
        full_match: bool,
        ignore_case: bool,
        cache: TextFilterCache
    ):
        self._texts = {i.lower() for i in texts} if ignore_case else set(texts)
        self._full_match = full_match
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
        texts = self._cache.get(event)

        if not self._texts:
            return bool(texts)

        for text in texts:
            if self._ignore_case:
                text = text.lower()

            if self._full_match:
                if text in self._texts:
                    return True
            else:
                if any(i in text for i in self._texts):
                    return True

        return False


class TextFilterFactory(AbstractEventFilterFactory):

    def __init__(self):
        self._cache = TextFilterCache()

    def get_filter(
        self,
        *texts: str,
        full_match: bool = True,
        ignore_case: bool = False
    ) -> TextFilter:
        return TextFilter(texts, full_match, ignore_case, self._cache)
