from dataclasses import dataclass

from telebox.bot.types.type import Type


@dataclass
class UserShared(Type):
    request_id: int
    user_id: int
