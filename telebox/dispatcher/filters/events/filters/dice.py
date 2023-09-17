from telebox.dispatcher.filters.events.filter import AbstractEventFilter
from telebox.dispatcher.enums.event_type import EventType
from telebox.bot.types.types.message import Message


class DiceFilter(AbstractEventFilter):

    def __init__(self, *emojis: str):
        self._emojis = set(emojis)

    def get_event_types(self) -> set[EventType]:
        return {EventType.MESSAGE, EventType.CHANNEL_POST}

    def check_event(self, event: Message) -> bool:
        if event.dice is not None:
            if self._emojis:
                return event.dice.emoji in self._emojis

            return True

        return False
