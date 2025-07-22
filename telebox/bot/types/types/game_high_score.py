from attrs import define

from telebox.bot.types.type import Type
from telebox.bot.types.types.user import User


@define(repr=False)
class GameHighScore(Type):
    position: int
    user: User
    score: int
