from dataclasses import dataclass
from typing import Optional

from telebox.bot.types.type import Type
from telebox.bot.types.types.sticker import Sticker
from telebox.bot.types.types.photo_size import PhotoSize


@dataclass(eq=False)
class StickerSet(Type):
    name: str
    title: str
    sticker_type: str
    is_animated: bool
    is_video: bool
    stickers: list[Sticker]
    thumb: Optional[PhotoSize] = None
