from dataclasses import dataclass

from telebox.bot.types.type import Type


@dataclass(repr=False)
class UsersShared(Type):
    request_id: int
    user_ids: list[int]
