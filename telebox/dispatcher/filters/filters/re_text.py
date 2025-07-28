from typing import Pattern, Union

from telebox.dispatcher.filters.filter import AbstractFilter
from telebox.dispatcher.enums.event_type import EventType
from telebox.dispatcher.utils.media_group import MediaGroup
from telebox.bot.types.message import Message


class RETextFilter(AbstractFilter):

    def __init__(self, *patterns: Pattern, full_match: bool = False):
        if not patterns:
            raise ValueError("No patterns!")

        self._patterns = patterns
        self._full_match = full_match

    def get_event_types(self) -> set[EventType]:
        return {
            EventType.MESSAGE,
            EventType.EDITED_MESSAGE,
            EventType.CHANNEL_POST,
            EventType.EDITED_CHANNEL_POST,
            EventType.MEDIA_GROUP,
            EventType.CHANNEL_MEDIA_GROUP
        }

    def get_value(self, event: Union[Message, MediaGroup]) -> list[str]:
        texts = []
        messages = event.messages if isinstance(event, MediaGroup) else [event]

        for i in messages:
            text = i.get_text()

            if text is not None:
                texts.append(text)

        return texts

    def check_value(self, value: list[str]) -> bool:
        for text in value:
            if self._full_match:
                if any(i.fullmatch(text) is not None for i in self._patterns):
                    return True
            else:
                if any(i.search(text) is not None for i in self._patterns):
                    return True

        return False
