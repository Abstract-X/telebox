from attrs import define

from telebox.bot.types.type import Type
from telebox.bot.types.types.paid_media import PaidMedia


@define(repr=False)
class PaidMediaInfo(Type):
    star_count: int
    paid_media: list[PaidMedia]
