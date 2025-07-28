from typing import Optional, Literal

from attrs import define

from telebox.bot.type import Type
from telebox.bot.types.document import Document
from telebox.bot.consts import background_types


@define(repr=False)
class BackgroundTypeWallpaper(Type):
    document: Document
    dark_theme_dimming: int
    is_blurred: Optional[Literal[True]] = None
    is_moving: Optional[Literal[True]] = None
    type: str = background_types.WALLPAPER
