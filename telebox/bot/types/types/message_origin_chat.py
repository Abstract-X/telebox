from typing import Optional
from dataclasses import dataclass
from datetime import datetime

from telebox.bot.types.type import Type
from telebox.bot.types.types.chat import Chat


@dataclass
class MessageOriginChat(Type):
    date: datetime
    sender_chat: Chat
    author_signature: Optional[str] = None
    type: str = "chat"
