from dataclasses import dataclass

from telebox.bot.types.type import Type
from telebox.bot.types.types.background_fill import BackgroundFill
from telebox.bot.consts import background_types


@dataclass(repr=False)
class BackgroundTypeFill(Type):
    fill: BackgroundFill
    dark_theme_dimming: int
    type: str = background_types.FILL
