from typing import Pattern, Union

from telebox.dispatcher.filters.event_filter import AbstractEventFilter
from telebox.dispatcher.enums.event_type import EventType
from telebox.dispatcher.utils.media_group import MediaGroup
from telebox.bot.types.types.message import Message


class RegExpTextFilter(AbstractEventFilter):

    def __init__(self, *patterns: Pattern, full_match: bool = True):
        self._patterns = patterns
        self._full_match = full_match

    def get_event_types(self) -> set[EventType]:
        return {
            EventType.MESSAGE,
            EventType.EDITED_MESSAGE,
            EventType.CHANNEL_POST,
            EventType.EDITED_CHANNEL_POST,
            EventType.MEDIA_GROUP
        }

    def get_value(self, event: Union[Message, MediaGroup]) -> list[str]:
        if isinstance(event, MediaGroup):
            messages = event.messages
        else:
            messages = [event]

        texts = []

        for i in messages:
            text = i.get_text()

            if text is not None:
                texts.append(text)

        return texts

    def check_value(self, value: set[str]) -> bool:
        if not self._patterns:
            return bool(value)

        for text in value:
            if self._full_match:
                if any(i.fullmatch(text) is not None for i in self._patterns):
                    return True
            else:
                if any(i.match(text) is not None for i in self._patterns):
                    return True

        return False
