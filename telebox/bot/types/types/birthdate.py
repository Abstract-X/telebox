from dataclasses import dataclass

from telebox.bot.types.type import Type


@dataclass(repr=False)
class Birthdate(Type):
    day: int
    month: int
    year: int
