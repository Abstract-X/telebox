from typing import Optional

from attrs import define

from telebox.bot.types.type import Type
from telebox.bot.types.types.sticker import Sticker


@define(repr=False)
class BusinessIntro(Type):
    title: Optional[str] = None
    message: Optional[str] = None
    sticker: Optional[Sticker] = None
