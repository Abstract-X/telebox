from typing import Optional
from datetime import datetime

from attrs import define

from telebox.bot.types.type import Type
from telebox.bot.types.types.chat import Chat


@define(repr=False)
class MessageOriginChannel(Type):
    date: datetime
    chat: Chat
    message_id: int
    author_signature: Optional[str] = None
    type: str = "channel"
