from dataclasses import dataclass
from datetime import datetime

from telebox.bot.types.type import Type


@dataclass(repr=False)
class MessageOriginHiddenUser(Type):
    date: datetime
    sender_user_name: str
    type: str = "hidden_user"
