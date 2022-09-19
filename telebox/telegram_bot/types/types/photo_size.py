from dataclasses import dataclass
from typing import Optional

from telebox.telegram_bot.types.base import Type


@dataclass(unsafe_hash=True)
class PhotoSize(Type):
    file_id: str
    file_unique_id: str
    width: int
    height: int
    file_size: Optional[int] = None
