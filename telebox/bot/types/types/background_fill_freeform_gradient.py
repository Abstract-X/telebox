from attrs import define

from telebox.bot.types.type import Type
from telebox.bot.consts import background_fill_types


@define(repr=False)
class BackgroundFillFreeformGradient(Type):
    colors: list[int]
    type: str = background_fill_types.FREEFORM_GRADIENT
