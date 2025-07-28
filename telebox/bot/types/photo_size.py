from typing import Optional

from attrs import define

from telebox.bot.type import Type


@define(repr=False)
class PhotoSize(Type):
    file_id: str
    file_unique_id: str
    width: int
    height: int
    file_size: Optional[int] = None
