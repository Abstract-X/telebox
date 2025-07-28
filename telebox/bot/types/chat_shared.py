from typing import Optional

from attrs import define

from telebox.bot.type import Type
from telebox.bot.types.photo_size import PhotoSize


@define(repr=False)
class ChatShared(Type):
    request_id: int
    chat_id: int
    title: Optional[str] = None
    username: Optional[str] = None
    photo: Optional[list[PhotoSize]] = None
