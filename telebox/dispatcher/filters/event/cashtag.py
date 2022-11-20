from typing import Union

from telebox.dispatcher.filters.event_filter import AbstractEventFilter
from telebox.dispatcher.enums.event_type import EventType
from telebox.dispatcher.utils.media_group import MediaGroup
from telebox.bot.types.types.message import Message
from telebox.bot.consts import message_entity_types


class CashtagFilter(AbstractEventFilter):

    def __init__(self, *cashtags: str):
        self._cashtags = set()

        for i in cashtags:
            if not i.startswith("$"):
                i = f"${i}"

            self._cashtags.add(i.upper())

    def get_event_types(self) -> set[EventType]:
        return {
            EventType.MESSAGE,
            EventType.EDITED_MESSAGE,
            EventType.CHANNEL_POST,
            EventType.EDITED_CHANNEL_POST,
            EventType.MEDIA_GROUP
        }

    def get_value(self, event: Union[Message, MediaGroup]) -> set[str]:
        cashtags = set()

        if isinstance(event, MediaGroup):
            for i in event:
                _gather_cashtags(i, cashtags)
        else:
            _gather_cashtags(event, cashtags)

        return cashtags

    def check_value(self, value: set[str]) -> bool:
        return any(i in self._cashtags for i in value) if self._cashtags else bool(value)


def _gather_cashtags(message: Message, cashtags: set[str]) -> None:
    for i in message.get_entities():
        if i.type == message_entity_types.CASHTAG:
            cashtags.add(message.get_entity_text(i))
