from dataclasses import dataclass
from datetime import datetime

from telebox.bot.types.type import Type
from telebox.bot.types.types.user import User


@dataclass
class MessageOriginUser(Type):
    date: datetime
    sender_user: User
    type: str = "user"
