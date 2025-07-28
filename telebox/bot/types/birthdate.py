from attrs import define

from telebox.bot.type import Type


@define(repr=False)
class Birthdate(Type):
    day: int
    month: int
    year: int
