from typing import Union

from telebox.dispatcher.filter import AbstractFilter
from telebox.dispatcher.types.media_group import MediaGroup
from telebox.bot.types.message import Message
from telebox.bot.consts import message_entity_types


class MentionFilter(AbstractFilter):
    def __init__(self, *mentions: str):
        self._mentions: set[str] = set()

        for i in mentions:
            if not i.startswith("@"):
                i = f"@{i}"

            self._mentions.add(i.lower())

    def get_value(self, event: Union[Message, MediaGroup]) -> set[str]:
        mentions = set()
        messages = event.messages if isinstance(event, MediaGroup) else [event]

        for message in messages:
            for entity in message.get_entities():
                if entity.type == message_entity_types.MENTION:
                    mentions.add(
                        message.get_entity_text(entity).lower()
                    )

        return mentions

    def check_value(self, value: set[str]) -> bool:
        if self._mentions:
            return any(i in self._mentions for i in value)

        return bool(value)
