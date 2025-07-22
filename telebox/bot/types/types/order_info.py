from typing import Optional

from attrs import define

from telebox.bot.types.type import Type
from telebox.bot.types.types.shipping_address import ShippingAddress


@define(repr=False)
class OrderInfo(Type):
    name: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None
    shipping_address: Optional[ShippingAddress] = None
