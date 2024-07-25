from dataclasses import dataclass
from typing import Optional

from telebox.bot.types.type import Type
from telebox.bot.types.types.photo_size import PhotoSize


@dataclass(repr=False)
class ChatShared(Type):
    request_id: int
    chat_id: int
    title: Optional[str] = None
    username: Optional[str] = None
    photo: Optional[list[PhotoSize]] = None
