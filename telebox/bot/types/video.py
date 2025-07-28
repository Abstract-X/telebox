from typing import Optional

from attrs import define

from telebox.bot.type import Type
from telebox.bot.types.photo_size import PhotoSize


@define(repr=False)
class Video(Type):
    file_id: str
    file_unique_id: str
    width: int
    height: int
    duration: int
    thumbnail: Optional[PhotoSize] = None
    file_name: Optional[str] = None
    mime_type: Optional[str] = None
    file_size: Optional[int] = None
