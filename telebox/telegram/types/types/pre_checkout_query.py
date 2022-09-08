from dataclasses import dataclass
from typing import Optional

from telebox.telegram.types.base import Type
from telebox.telegram.types.types.user import User
from telebox.telegram.types.types.order_info import OrderInfo


@dataclass(unsafe_hash=True)
class PreCheckoutQuery(Type):
    id: str
    from_: User
    currency: str
    total_amount: int
    invoice_payload: str
    shipping_option_id: Optional[str] = None
    order_info: Optional[OrderInfo] = None
