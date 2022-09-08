from dataclasses import dataclass

from telebox.telegram.types.base import Type
from telebox.telegram.types.types.user import User
from telebox.telegram.types.types.shipping_address import ShippingAddress


@dataclass(unsafe_hash=True)
class ShippingQuery(Type):
    id: str
    from_: User
    invoice_payload: str
    shipping_address: ShippingAddress
