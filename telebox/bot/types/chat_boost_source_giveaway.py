from typing import Optional, Literal

from attrs import define

from telebox.bot.type import Type
from telebox.bot.types.user import User


@define(repr=False)
class ChatBoostSourceGiveaway(Type):
    giveaway_message_id: int
    user: Optional[User] = None
    is_unclaimed: Optional[Literal[True]] = None
    source: str = "giveaway"
