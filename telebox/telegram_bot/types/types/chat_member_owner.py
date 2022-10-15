from dataclasses import dataclass
from typing import Optional

from telebox.telegram_bot.types.type import Type
from telebox.telegram_bot.consts import chat_member_statuses
from telebox.telegram_bot.types.types.user import User


@dataclass(unsafe_hash=True)
class ChatMemberOwner(Type):
    user: User
    is_anonymous: bool
    custom_title: Optional[str] = None
    status: str = chat_member_statuses.CREATOR
