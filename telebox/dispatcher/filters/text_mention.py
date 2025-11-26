from typing import Union

from telebox.dispatcher.filter import AbstractFilter
from telebox.dispatcher.types.media_group import MediaGroup
from telebox.bot.types.message import Message
from telebox.bot.consts import message_entity_types


class TextMentionFilter(AbstractFilter):
    def __init__(self, *mentions: str):
        self._mentions = {i.lower() for i in mentions}

    def get_value(self, event: Union[Message, MediaGroup]) -> set[str]:
        mentions = set()
        messages = event.messages if isinstance(event, MediaGroup) else [event]

        for message in messages:
            for entity in message.get_entities():
                if entity.type == message_entity_types.TEXT_MENTION:
                    mentions.add(
                        message.get_entity_text(entity).lower()
                    )

        return mentions

    def check_value(self, value: set[str]) -> bool:
        if self._mentions:
            return any(i in self._mentions for i in value)

        return bool(value)
