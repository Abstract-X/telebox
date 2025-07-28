from datetime import datetime

from attrs import define

from telebox.bot.type import Type
from telebox.bot.types.user import User


@define(repr=False)
class MessageOriginUser(Type):
    date: datetime
    sender_user: User
    type: str = "user"
