from datetime import datetime
from typing import Optional

from attrs import define

from telebox.bot.type import Type
from telebox.bot.consts import chat_member_statuses
from telebox.bot.types.user import User


@define(repr=False)
class ChatMemberBanned(Type):
    user: User
    until_date: Optional[datetime] = None  # None instead of 0
    status: str = chat_member_statuses.KICKED
