from telebox.dispatcher.filters.event_filter import AbstractEventFilter
from telebox.dispatcher.dispatcher import Event
from telebox.dispatcher.enums.event_type import EventType
from telebox.telegram_bot.types.types.message import Message
from telebox.telegram_bot.consts import message_entity_types


class CashtagFilter(AbstractEventFilter):

    def __init__(self, *cashtags: str):
        self._cashtags = set()

        for i in cashtags:
            if not i.startswith("$"):
                i = f"${i}"

            self._cashtags.add(i.upper())

    def get_value(self, event: Event, event_type: EventType) -> set[str]:
        cashtags = set()

        if isinstance(event, Message):
            for i in event.get_entities():
                if i.type == message_entity_types.CASHTAG:
                    cashtags.add(event.get_entity_text(i))

        return cashtags

    def check_value(self, value: set[str]) -> bool:
        return any(i in self._cashtags for i in value) if self._cashtags else bool(value)
