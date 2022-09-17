from dataclasses import dataclass
from typing import Optional

from telebox.telegram_bot.types.base import Type
from telebox.telegram_bot.types.types.photo_size import PhotoSize


@dataclass(unsafe_hash=True)
class VideoNote(Type):
    file_id: str
    file_unique_id: str
    length: int
    duration: int
    thumb: Optional[PhotoSize] = None
    file_size: Optional[int] = None
