from typing import Optional

from attrs import define

from telebox.bot.type import Type


@define(repr=False)
class GiveawayCreated(Type):
    prize_star_count: Optional[int] = None
