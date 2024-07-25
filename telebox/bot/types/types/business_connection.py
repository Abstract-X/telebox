from dataclasses import dataclass
from datetime import datetime

from telebox.bot.types.type import Type
from telebox.bot.types.types.user import User


@dataclass(repr=False)
class BusinessConnection(Type):
    id: str
    user: User
    user_chat_id: int
    date: datetime
    can_reply: bool
    is_enabled: bool
