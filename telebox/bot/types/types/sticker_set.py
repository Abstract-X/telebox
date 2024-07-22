from dataclasses import dataclass
from typing import Optional

from telebox.bot.types.type import Type
from telebox.bot.types.types.sticker import Sticker
from telebox.bot.types.types.photo_size import PhotoSize


@dataclass(repr=False)
class StickerSet(Type):
    name: str
    title: str
    sticker_type: str
    stickers: list[Sticker]
    thumbnail: Optional[PhotoSize] = None
