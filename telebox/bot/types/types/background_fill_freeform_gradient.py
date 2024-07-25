from dataclasses import dataclass

from telebox.bot.types.type import Type
from telebox.bot.consts import background_fill_types


@dataclass(repr=False)
class BackgroundFillFreeformGradient(Type):
    colors: list[int]
    type: str = background_fill_types.FREEFORM_GRADIENT
