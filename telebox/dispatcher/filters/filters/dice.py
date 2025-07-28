from typing import Optional

from telebox.dispatcher.filters.filter import AbstractFilter
from telebox.dispatcher.enums.event_type import EventType
from telebox.bot.types.message import Message
from telebox.bot.types.dice import Dice


class DiceFilter(AbstractFilter):

    def __init__(self, *emojis: str):
        self._emojis = set(emojis)

    def get_event_types(self) -> set[EventType]:
        return {EventType.MESSAGE, EventType.CHANNEL_POST}

    def get_value(self, event: Message) -> Optional[Dice]:
        return event.dice

    def check_value(self, value: Optional[Dice]) -> bool:
        if value is not None:
            if self._emojis:
                return value.emoji in self._emojis

            return True

        return False
