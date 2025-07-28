from datetime import datetime
from typing import Optional

from attrs import define

from telebox.bot.type import Type
from telebox.bot.types.chat import Chat


@define(repr=False)
class InaccessibleMessage(Type):
    chat: Chat
    message_id: int
    date: Optional[datetime] = None
