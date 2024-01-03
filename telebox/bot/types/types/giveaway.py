from dataclasses import dataclass
from datetime import datetime
from typing import Literal, Optional

from telebox.bot.types.type import Type
from telebox.bot.types.types.chat import Chat


@dataclass
class Giveaway(Type):
    chats: list[Chat]
    winners_selection_date: datetime
    winner_count: int
    only_new_members: Optional[Literal[True]] = None
    has_public_winners: Optional[Literal[True]] = None
    prize_description: Optional[str] = None
    country_codes: Optional[list[str]] = None
    premium_subscription_month_count: Optional[int] = None
