from dataclasses import dataclass

from telebox.bot.types.type import Type
from telebox.bot.types.types.user import User


@dataclass
class PollAnswer(Type):
    poll_id: str
    user: User
    option_ids: list[int]

    @property
    def user_id(self) -> int:
        return self.user.id
