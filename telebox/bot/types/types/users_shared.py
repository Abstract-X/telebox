from attrs import define

from telebox.bot.types.type import Type
from telebox.bot.types.types.shared_user import SharedUser


@define(repr=False)
class UsersShared(Type):
    request_id: int
    users: list[SharedUser]
