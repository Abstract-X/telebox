from attrs import define

from telebox.bot.type import Type


@define(repr=False)
class Dice(Type):
    emoji: str
    value: int
