from typing import Optional

from attrs import define

from telebox.bot.type import Type
from telebox.bot.types.order_info import OrderInfo


@define(repr=False)
class SuccessfulPayment(Type):
    currency: str
    total_amount: int
    invoice_payload: str
    telegram_payment_charge_id: str
    provider_payment_charge_id: str
    shipping_option_id: Optional[str] = None
    order_info: Optional[OrderInfo] = None
