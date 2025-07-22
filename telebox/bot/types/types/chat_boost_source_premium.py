from attrs import define

from telebox.bot.types.type import Type
from telebox.bot.types.types.user import User


@define(repr=False)
class ChatBoostSourcePremium(Type):
    user: User
    source: str = "premium"
