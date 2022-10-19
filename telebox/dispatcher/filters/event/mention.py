from telebox.dispatcher.filters.event_filter import AbstractEventFilter
from telebox.dispatcher.dispatcher import Event
from telebox.dispatcher.enums.event_type import EventType
from telebox.telegram_bot.types.types.message import Message
from telebox.telegram_bot.consts import message_entity_types


class MentionFilter(AbstractEventFilter):

    def __init__(self, *mentions: str):
        self._mentions = set()

        for i in mentions:
            if not i.startswith("@"):
                i = f"@{i}"

            self._mentions.add(i)

    def get_value(self, event: Event, event_type: EventType) -> set[str]:
        mentions = set()

        if isinstance(event, Message):
            for i in event.get_entities():
                if i.type == message_entity_types.MENTION:
                    mentions.add(event.get_entity_text(i))

        return mentions

    def check_value(self, value: set[str]) -> bool:
        return any(i in self._mentions for i in value) if self._mentions else bool(value)
