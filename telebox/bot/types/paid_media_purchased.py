from attrs import define

from telebox.bot.type import Type
from telebox.bot.types.user import User


@define(repr=False)
class PaidMediaPurchased(Type):
    from_: User
    paid_media_payload: str
