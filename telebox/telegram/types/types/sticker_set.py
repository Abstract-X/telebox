from dataclasses import dataclass
from typing import Optional

from telebox.telegram.types.base import Type
from telebox.telegram.types.types.sticker import Sticker
from telebox.telegram.types.types.photo_size import PhotoSize


@dataclass(unsafe_hash=True)
class StickerSet(Type):
    name: str
    title: str
    sticker_type: str
    is_animated: bool
    is_video: bool
    stickers: list[Sticker]
    thumb: Optional[PhotoSize] = None
