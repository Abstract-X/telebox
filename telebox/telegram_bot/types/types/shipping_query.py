from dataclasses import dataclass

from telebox.telegram_bot.types.type import Type
from telebox.telegram_bot.types.types.user import User
from telebox.telegram_bot.types.types.shipping_address import ShippingAddress


@dataclass(unsafe_hash=True)
class ShippingQuery(Type):
    id: str
    from_: User
    invoice_payload: str
    shipping_address: ShippingAddress

    @property
    def user_id(self) -> int:
        return self.from_.id
