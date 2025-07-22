from typing import Optional

from attrs import define

from telebox.bot.types.type import Type


@define(repr=False)
class Voice(Type):
    file_id: str
    file_unique_id: str
    duration: int
    mime_type: Optional[str] = None
    file_size: Optional[int] = None
