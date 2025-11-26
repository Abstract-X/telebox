from typing import Union

from telebox.dispatcher.filter import AbstractFilter
from telebox.dispatcher.types.media_group import MediaGroup
from telebox.bot.types.message import Message
from telebox.bot.consts import message_entity_types


class CashtagFilter(AbstractFilter):
    def __init__(self, *cashtags: str):
        self._cashtags: set[str] = set()

        for i in cashtags:
            if not i.startswith("$"):
                i = f"${i}"

            self._cashtags.add(i.upper())

    def get_value(self, event: Union[Message, MediaGroup]) -> set[str]:
        cashtags = set()
        messages = event.messages if isinstance(event, MediaGroup) else [event]

        for message in messages:
            for entity in message.get_entities():
                if entity.type == message_entity_types.CASHTAG:
                    cashtags.add(
                        message.get_entity_text(entity)
                    )

        return cashtags

    def check_value(self, value: set[str]) -> bool:
        if self._cashtags:
            return any(i in self._cashtags for i in value)

        return bool(value)
