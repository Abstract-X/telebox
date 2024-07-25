from dataclasses import dataclass

from telebox.bot.types.type import Type
from telebox.bot.types.types.shared_user import SharedUser


@dataclass(repr=False)
class UsersShared(Type):
    request_id: int
    users: list[SharedUser]
