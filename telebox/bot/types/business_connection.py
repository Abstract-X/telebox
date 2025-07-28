from datetime import datetime

from attrs import define

from telebox.bot.type import Type
from telebox.bot.types.user import User


@define(repr=False)
class BusinessConnection(Type):
    id: str
    user: User
    user_chat_id: int
    date: datetime
    can_reply: bool
    is_enabled: bool
