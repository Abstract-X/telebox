from dataclasses import dataclass

from telebox.bot.types.type import Type


@dataclass
class Dice(Type):
    emoji: str
    value: int
