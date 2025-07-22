from datetime import datetime
from typing import Optional

from attrs import define

from telebox.bot.types.type import Type
from telebox.bot.types.types.chat import Chat


@define(repr=False)
class InaccessibleMessage(Type):
    chat: Chat
    message_id: int
    date: Optional[datetime] = None
