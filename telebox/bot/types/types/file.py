from typing import Optional

from attrs import define

from telebox.bot.types.type import Type


@define(repr=False)
class File(Type):
    file_id: str
    file_unique_id: str
    file_size: Optional[int] = None
    file_path: Optional[str] = None
