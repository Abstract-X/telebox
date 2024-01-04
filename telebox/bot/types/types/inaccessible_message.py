from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from telebox.bot.types.type import Type
from telebox.bot.types.types.chat import Chat


@dataclass
class InaccessibleMessage(Type):
    chat: Chat
    message_id: int
    date: Optional[datetime] = None
