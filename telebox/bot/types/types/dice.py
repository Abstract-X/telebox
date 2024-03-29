from dataclasses import dataclass

from telebox.bot.types.type import Type


@dataclass(repr=False)
class Dice(Type):
    emoji: str
    value: int
