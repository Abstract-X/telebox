from dataclasses import dataclass

from telebox.telegram.types.base import Type
from telebox.telegram.types.types.user import User


@dataclass(unsafe_hash=True)
class PollAnswer(Type):
    poll_id: str
    user: User
    option_ids: list[int]
