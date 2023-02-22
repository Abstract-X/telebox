from dataclasses import dataclass
from typing import Optional

from telebox.bot.types.type import Type
from telebox.bot.types.types.photo_size import PhotoSize
from telebox.bot.types.types.file import File
from telebox.bot.types.types.mask_position import MaskPosition


@dataclass
class Sticker(Type):
    file_id: str
    file_unique_id: str
    type: str
    width: int
    height: int
    is_animated: bool
    is_video: bool
    thumb: Optional[PhotoSize] = None
    emoji: Optional[str] = None
    set_name: Optional[str] = None
    premium_animation: Optional[File] = None
    mask_position: Optional[MaskPosition] = None
    custom_emoji_id: Optional[str] = None
    file_size: Optional[int] = None
