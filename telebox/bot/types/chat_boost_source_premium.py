from attrs import define

from telebox.bot.type import Type
from telebox.bot.types.user import User


@define(repr=False)
class ChatBoostSourcePremium(Type):
    user: User
    source: str = "premium"
