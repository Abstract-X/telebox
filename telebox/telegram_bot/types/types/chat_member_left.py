from dataclasses import dataclass

from telebox.telegram_bot.types.base import Type
from telebox.telegram_bot.consts import chat_member_statuses
from telebox.telegram_bot.types.types.user import User


@dataclass(unsafe_hash=True)
class ChatMemberLeft(Type):
    user: User
    status: str = chat_member_statuses.LEFT
