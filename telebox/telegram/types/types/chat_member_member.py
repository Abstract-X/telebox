from dataclasses import dataclass

from telebox.telegram.types.base import Type
from telebox.telegram.consts import chat_member_statuses
from telebox.telegram.types.types.user import User


@dataclass(unsafe_hash=True)
class ChatMemberMember(Type):
    user: User
    status: str = chat_member_statuses.MEMBER
