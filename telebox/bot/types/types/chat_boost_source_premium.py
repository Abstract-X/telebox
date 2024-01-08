from dataclasses import dataclass

from telebox.bot.types.type import Type
from telebox.bot.types.types.user import User


@dataclass
class ChatBoostSourcePremium(Type):
    user: User
    source: str = "premium"
