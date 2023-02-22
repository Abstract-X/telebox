from dataclasses import dataclass
from typing import Optional

from telebox.bot.types.type import Type


@dataclass
class File(Type):
    file_id: str
    file_unique_id: str
    file_size: Optional[int] = None
    file_path: Optional[str] = None
