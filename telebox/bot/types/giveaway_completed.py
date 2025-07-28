from typing import Optional, Literal

from attrs import define

from telebox.bot.type import Type
from telebox.bot.types.message import Message


@define(repr=False)
class GiveawayCompleted(Type):
    winner_count: int
    unclaimed_prize_count: Optional[int] = None
    giveaway_message: Optional[Message] = None
    is_star_giveaway: Optional[Literal[True]] = None
