from dataclasses import dataclass

from telebox.bot.types.type import Type
from telebox.bot.consts import background_fill_types


@dataclass(repr=False)
class BackgroundFillSolid(Type):
    color: int
    type: str = background_fill_types.SOLID
