from dataclasses import dataclass
from typing import Optional

from telebox.bot.types.type import Type


@dataclass
class PhotoSize(Type):
    file_id: str
    file_unique_id: str
    width: int
    height: int
    file_size: Optional[int] = None
