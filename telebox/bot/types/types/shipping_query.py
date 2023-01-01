from dataclasses import dataclass

from telebox.bot.types.type import Type
from telebox.bot.types.types.user import User
from telebox.bot.types.types.shipping_address import ShippingAddress


@dataclass(eq=False)
class ShippingQuery(Type):
    id: str
    from_: User
    invoice_payload: str
    shipping_address: ShippingAddress

    @property
    def user_id(self) -> int:
        return self.from_.id
