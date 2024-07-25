from dataclasses import dataclass
from typing import Optional, Literal

from telebox.bot.types.type import Type
from telebox.bot.types.types.document import Document
from telebox.bot.types.types.background_fill import BackgroundFill
from telebox.bot.consts import background_types


@dataclass(repr=False)
class BackgroundTypePattern(Type):
    document: Document
    fill: BackgroundFill
    intensity: int
    is_inverted: Optional[Literal[True]] = None
    is_moving: Optional[Literal[True]] = None
    type: str = background_types.PATTERN
