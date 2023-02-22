from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from telebox.bot.types.type import Type
from telebox.bot.consts import chat_member_statuses
from telebox.bot.types.types.user import User


@dataclass
class ChatMemberBanned(Type):
    user: User
    until_date: Optional[datetime] = None  # None instead of 0
    status: str = chat_member_statuses.KICKED
