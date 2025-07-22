from attrs import define

from telebox.bot.types.type import Type


@define(repr=False)
class Dice(Type):
    emoji: str
    value: int
