from attrs import define

from telebox.bot.type import Type
from telebox.bot.consts import chat_member_statuses
from telebox.bot.types.user import User


@define(repr=False)
class ChatMemberLeft(Type):
    user: User
    status: str = chat_member_statuses.LEFT
