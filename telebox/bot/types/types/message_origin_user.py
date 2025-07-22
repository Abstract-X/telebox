from datetime import datetime

from attrs import define

from telebox.bot.types.type import Type
from telebox.bot.types.types.user import User


@define(repr=False)
class MessageOriginUser(Type):
    date: datetime
    sender_user: User
    type: str = "user"
