from dataclasses import dataclass
from typing import Optional

from telebox.bot.types.type import Type
from telebox.bot.types.types.sticker import Sticker


@dataclass(repr=False)
class BusinessIntro(Type):
    title: Optional[str] = None
    message: Optional[str] = None
    sticker: Optional[Sticker] = None
