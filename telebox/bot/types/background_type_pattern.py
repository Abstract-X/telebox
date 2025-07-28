from typing import Optional, Literal

from attrs import define

from telebox.bot.type import Type
from telebox.bot.types.document import Document
from telebox.bot.types.background_fill import BackgroundFill
from telebox.bot.consts import background_types


@define(repr=False)
class BackgroundTypePattern(Type):
    document: Document
    fill: BackgroundFill
    intensity: int
    is_inverted: Optional[Literal[True]] = None
    is_moving: Optional[Literal[True]] = None
    type: str = background_types.PATTERN
