from dataclasses import dataclass

from telebox.bot.types.type import Type
from telebox.bot.consts import chat_member_statuses
from telebox.bot.types.types.user import User


@dataclass
class ChatMemberMember(Type):
    user: User
    status: str = chat_member_statuses.MEMBER
