from dataclasses import dataclass

from telebox.bot.types.type import Type
from telebox.bot.consts import background_fill_types


@dataclass(repr=False)
class BackgroundFillGradient(Type):
    top_color: int
    bottom_color: int
    rotation_angle: int
    type: str = background_fill_types.GRADIENT
