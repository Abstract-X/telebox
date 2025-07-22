from attrs import define

from telebox.bot.types.type import Type


@define(repr=False)
class Birthdate(Type):
    day: int
    month: int
    year: int
