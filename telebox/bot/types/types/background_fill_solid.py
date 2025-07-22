from attrs import define

from telebox.bot.types.type import Type
from telebox.bot.consts import background_fill_types


@define(repr=False)
class BackgroundFillSolid(Type):
    color: int
    type: str = background_fill_types.SOLID
