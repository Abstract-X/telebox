from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from telebox.telegram.types.base import Type
from telebox.telegram.consts import chat_member_statuses
from telebox.telegram.types.types.user import User


@dataclass(unsafe_hash=True)
class ChatMemberBanned(Type):
    user: User
    until_date: Optional[datetime] = None  # None instead of 0
    status: str = chat_member_statuses.KICKED
