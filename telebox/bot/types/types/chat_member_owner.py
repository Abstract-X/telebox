from dataclasses import dataclass
from typing import Optional

from telebox.bot.types.type import Type
from telebox.bot.consts import chat_member_statuses
from telebox.bot.types.types.user import User


@dataclass
class ChatMemberOwner(Type):
    user: User
    is_anonymous: bool
    custom_title: Optional[str] = None
    status: str = chat_member_statuses.CREATOR
