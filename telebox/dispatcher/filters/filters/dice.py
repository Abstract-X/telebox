from typing import Optional

from telebox.dispatcher.filters.filter import AbstractFilter
from telebox.bot.types.message import Message


class DiceFilter(AbstractFilter):
    def __init__(self, *emojis: str):
        self._emojis = set(emojis)

    def get_value(self, event: Message) -> Optional[str]:
        if event.dice is not None:
            return event.dice.emoji

    def check_value(self, value: Optional[str]) -> bool:
        if self._emojis:
            return value in self._emojis

        return value is not None
