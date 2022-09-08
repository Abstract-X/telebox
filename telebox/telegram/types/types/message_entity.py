from dataclasses import dataclass
from typing import Optional

from telebox.telegram.types.base import Type
from telebox.telegram.types.types.user import User


@dataclass(unsafe_hash=True)
class MessageEntity(Type):
    type: str
    offset: int
    length: int
    url: Optional[str] = None
    user: Optional[User] = None
    language: Optional[str] = None
    custom_emoji_id: Optional[str] = None
