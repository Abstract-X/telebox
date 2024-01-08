from dataclasses import dataclass
from typing import Optional, Literal

from telebox.bot.types.type import Type
from telebox.bot.types.types.user import User


@dataclass
class ChatBoostSourceGiveaway(Type):
    giveaway_message_id: int
    user: Optional[User] = None
    is_unclaimed: Optional[Literal[True]] = None
    source: str = "giveaway"
