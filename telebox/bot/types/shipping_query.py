from attrs import define

from telebox.bot.type import Type
from telebox.bot.types.user import User
from telebox.bot.types.shipping_address import ShippingAddress


@define(repr=False)
class ShippingQuery(Type):
    id: str
    from_: User
    invoice_payload: str
    shipping_address: ShippingAddress

    @property
    def user_id(self) -> int:
        return self.from_.id
