from dataclasses import dataclass

from telebox.bot.types.type import Type
from telebox.bot.types.types.user import User


@dataclass(unsafe_hash=True)
class GameHighScore(Type):
    position: int
    user: User
    score: int
