from typing import Union

from telebox.dispatcher.filters.filter import AbstractFilter
from telebox.dispatcher.enums.event_type import EventType
from telebox.dispatcher.utils.media_group import MediaGroup
from telebox.bot.types.message import Message
from telebox.bot.consts import message_entity_types


class HashtagFilter(AbstractFilter):

    def __init__(self, *hashtags: str, ignore_case: bool):
        self._hashtags = set()

        for i in hashtags:
            if not i.startswith("#"):
                i = f"#{i}"

            if ignore_case:
                i = i.lower()

            self._hashtags.add(i)

        self._ignore_case = ignore_case

    def get_event_types(self) -> set[EventType]:
        return {
            EventType.MESSAGE,
            EventType.EDITED_MESSAGE,
            EventType.CHANNEL_POST,
            EventType.EDITED_CHANNEL_POST,
            EventType.MEDIA_GROUP,
            EventType.CHANNEL_MEDIA_GROUP
        }

    def get_value(self, event: Union[Message, MediaGroup]) -> set[str]:
        hashtags = set()
        messages = event.messages if isinstance(event, MediaGroup) else [event]

        for message in messages:
            for entity in message.get_entities():
                if entity.type == message_entity_types.HASHTAG:
                    hashtags.add(
                        message.get_entity_text(entity)
                    )

        return hashtags

    def check_value(self, value: set[str]) -> bool:
        if not self._hashtags:
            return bool(value)

        for i in value:
            if self._ignore_case:
                i = i.lower()

            if i in self._hashtags:
                return True

        return False
