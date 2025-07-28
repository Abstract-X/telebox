from typing import Optional

from attrs import define

from telebox.bot.type import Type
from telebox.bot.types.sticker import Sticker
from telebox.bot.types.photo_size import PhotoSize


@define(repr=False)
class StickerSet(Type):
    name: str
    title: str
    sticker_type: str
    stickers: list[Sticker]
    thumbnail: Optional[PhotoSize] = None
