from dataclasses import dataclass
from typing import Optional

from telebox.bot.types.type import Type
from telebox.bot.types.types.photo_size import PhotoSize


@dataclass(repr=False)
class SharedUser(Type):
    user_id: int
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None
    photo: Optional[list[PhotoSize]] = None
