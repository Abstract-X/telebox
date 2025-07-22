from typing import Optional

from attrs import define

from telebox.bot.types.type import Type
from telebox.bot.types.types.user import User


@define(repr=False)
class MessageEntity(Type):
    type: str
    offset: int
    length: int
    url: Optional[str] = None
    user: Optional[User] = None
    language: Optional[str] = None
    custom_emoji_id: Optional[str] = None

    @property
    def end_offset(self) -> int:
        return self.offset + self.length
