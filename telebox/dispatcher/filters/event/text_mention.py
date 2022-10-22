from telebox.dispatcher.filters.event_filter import AbstractEventFilter
from telebox.dispatcher.typing import Event
from telebox.dispatcher.enums.event_type import EventType
from telebox.telegram_bot.types.types.message import Message
from telebox.telegram_bot.consts import message_entity_types


class TextMentionFilter(AbstractEventFilter):

    def __init__(self, *mentions: str):
        self._mentions = {i.lower() for i in mentions}

    def get_value(self, event: Event, event_type: EventType) -> set[str]:
        mentions = set()

        if isinstance(event, Message):
            for i in event.get_entities():
                if i.type == message_entity_types.TEXT_MENTION:
                    mentions.add(event.get_entity_text(i).lower())

        return mentions

    def check_value(self, value: set[str]) -> bool:
        return any(i in self._mentions for i in value) if self._mentions else bool(value)
