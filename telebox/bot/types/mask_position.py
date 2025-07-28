from attrs import define

from telebox.bot.type import Type


@define(repr=False)
class MaskPosition(Type):
    point: str
    x_shift: float
    y_shift: float
    scale: float
