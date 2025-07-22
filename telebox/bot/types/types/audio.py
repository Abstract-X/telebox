from typing import Optional

from attrs import define

from telebox.bot.types.type import Type
from telebox.bot.types.types.photo_size import PhotoSize


@define(repr=False)
class Audio(Type):
    file_id: str
    file_unique_id: str
    duration: int
    performer: Optional[str] = None
    title: Optional[str] = None
    file_name: Optional[str] = None
    mime_type: Optional[str] = None
    file_size: Optional[int] = None
    thumbnail: Optional[PhotoSize] = None
