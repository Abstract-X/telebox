from dataclasses import dataclass

from telebox.telegram_bot.types.base import Type
from telebox.telegram_bot.types.types.user import User


@dataclass(unsafe_hash=True)
class PollAnswer(Type):
    poll_id: str
    user: User
    option_ids: list[int]

    @property
    def user_id(self) -> int:
        return self.user.id
