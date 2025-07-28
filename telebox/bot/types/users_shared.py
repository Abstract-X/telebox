from attrs import define

from telebox.bot.type import Type
from telebox.bot.types.shared_user import SharedUser


@define(repr=False)
class UsersShared(Type):
    request_id: int
    users: list[SharedUser]
