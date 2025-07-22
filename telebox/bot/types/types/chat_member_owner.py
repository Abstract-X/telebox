from typing import Optional

from attrs import define

from telebox.bot.types.type import Type
from telebox.bot.consts import chat_member_statuses
from telebox.bot.types.types.user import User


@define(repr=False)
class ChatMemberOwner(Type):
    user: User
    is_anonymous: bool
    custom_title: Optional[str] = None
    status: str = chat_member_statuses.CREATOR
