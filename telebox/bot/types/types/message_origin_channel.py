from typing import Optional
from dataclasses import dataclass
from datetime import datetime

from telebox.bot.types.type import Type
from telebox.bot.types.types.chat import Chat


@dataclass
class MessageOriginChannel(Type):
    date: datetime
    chat: Chat
    message_id: int
    author_signature: Optional[str] = None
    type: str = "channel"
