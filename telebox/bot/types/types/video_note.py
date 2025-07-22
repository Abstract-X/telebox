from typing import Optional

from attrs import define

from telebox.bot.types.type import Type
from telebox.bot.types.types.photo_size import PhotoSize


@define(repr=False)
class VideoNote(Type):
    file_id: str
    file_unique_id: str
    length: int
    duration: int
    thumbnail: Optional[PhotoSize] = None
    file_size: Optional[int] = None
