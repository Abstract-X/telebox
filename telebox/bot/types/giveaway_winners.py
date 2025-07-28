from datetime import datetime
from typing import Optional, Literal

from attrs import define

from telebox.bot.type import Type
from telebox.bot.types.chat import Chat
from telebox.bot.types.user import User


@define(repr=False)
class GiveawayWinners(Type):
    chat: Chat
    giveaway_message_id: int
    winners_selection_date: datetime
    winner_count: int
    winners: list[User]
    additional_chat_count: Optional[int] = None
    premium_subscription_month_count: Optional[int] = None
    unclaimed_prize_count: Optional[int] = None
    only_new_members: Optional[Literal[True]] = None
    was_refunded: Optional[Literal[True]] = None
    prize_description: Optional[str] = None
