from datetime import datetime
from typing import Literal, Optional

from attrs import define

from telebox.bot.type import Type
from telebox.bot.types.chat import Chat


@define(repr=False)
class Giveaway(Type):
    chats: list[Chat]
    winners_selection_date: datetime
    winner_count: int
    only_new_members: Optional[Literal[True]] = None
    has_public_winners: Optional[Literal[True]] = None
    prize_description: Optional[str] = None
    country_codes: Optional[list[str]] = None
    prize_star_count: Optional[int] = None
    premium_subscription_month_count: Optional[int] = None
