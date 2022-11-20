from typing import Union

from telebox.dispatcher.filters.event_filter import AbstractEventFilter
from telebox.dispatcher.enums.event_type import EventType
from telebox.dispatcher.utils.media_group import MediaGroup
from telebox.bot.types.types.message import Message


class TextFilter(AbstractEventFilter):

    def __init__(self, *texts: str, full_match: bool = True, ignore_case: bool = False):
        self._texts = {i.lower() for i in texts} if ignore_case else set(texts)
        self._full_match = full_match
        self._ignore_case = ignore_case

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

    def check_value(self, value: list[str]) -> bool:
        if not self._texts:
            return bool(value)

        for text in value:
            if self._ignore_case:
                text = text.lower()

            if self._full_match:
                if text in self._texts:
                    return True
            else:
                if any(i in text for i in self._texts):
                    return True

        return False
