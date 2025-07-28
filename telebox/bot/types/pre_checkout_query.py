from typing import Optional

from attrs import define

from telebox.bot.type import Type
from telebox.bot.types.user import User
from telebox.bot.types.order_info import OrderInfo


@define(repr=False)
class PreCheckoutQuery(Type):
    id: str
    from_: User
    currency: str
    total_amount: int
    invoice_payload: str
    shipping_option_id: Optional[str] = None
    order_info: Optional[OrderInfo] = None

    @property
    def user_id(self) -> int:
        return self.from_.id
