from datetime import datetime
from typing import Optional

from attrs import define

from telebox.bot.types.type import Type
from telebox.bot.consts import chat_member_statuses
from telebox.bot.types.types.user import User


@define(repr=False)
class ChatMemberMember(Type):
    user: User
    status: str = chat_member_statuses.MEMBER
    until_date: Optional[datetime] = None
