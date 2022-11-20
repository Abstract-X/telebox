from typing import Union

from telebox.dispatcher.filters.event_filter import AbstractEventFilter
from telebox.dispatcher.enums.event_type import EventType
from telebox.dispatcher.utils.media_group import MediaGroup
from telebox.bot.types.types.message import Message
from telebox.bot.consts import message_entity_types


class TextMentionFilter(AbstractEventFilter):

    def __init__(self, *mentions: str):
        self._mentions = {i.lower() for i in mentions}

    def get_event_types(self) -> set[EventType]:
        return {
            EventType.MESSAGE,
            EventType.EDITED_MESSAGE,
            EventType.CHANNEL_POST,
            EventType.EDITED_CHANNEL_POST,
            EventType.MEDIA_GROUP
        }

    def get_value(self, event: Union[Message, MediaGroup]) -> set[str]:
        mentions = set()

        if isinstance(event, MediaGroup):
            for i in event:
                _gather_mentions(i, mentions)
        else:
            _gather_mentions(event, mentions)

        return mentions

    def check_value(self, value: set[str]) -> bool:
        return any(i in self._mentions for i in value) if self._mentions else bool(value)


def _gather_mentions(message: Message, mentions: set[str]) -> None:
    for i in message.get_entities():
        if i.type == message_entity_types.TEXT_MENTION:
            mentions.add(message.get_entity_text(i).lower())
