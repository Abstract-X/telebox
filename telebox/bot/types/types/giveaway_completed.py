from dataclasses import dataclass
from typing import Optional

from telebox.bot.types.type import Type
from telebox.bot.types.types.message import Message


@dataclass
class GiveawayCompleted(Type):
    winner_count: int
    unclaimed_prize_count: Optional[int] = None
    giveaway_message: Optional[Message] = None
