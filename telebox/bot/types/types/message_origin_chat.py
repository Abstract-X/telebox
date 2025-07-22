from typing import Optional
from datetime import datetime

from attrs import define

from telebox.bot.types.type import Type
from telebox.bot.types.types.chat import Chat


@define(repr=False)
class MessageOriginChat(Type):
    date: datetime
    sender_chat: Chat
    author_signature: Optional[str] = None
    type: str = "chat"
