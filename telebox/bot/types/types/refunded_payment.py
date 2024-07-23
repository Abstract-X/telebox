from dataclasses import dataclass
from typing import Optional

from telebox.bot.types.type import Type


@dataclass(repr=False)
class RefundedPayment(Type):
    currency: str
    total_amount: int
    invoice_payload: str
    telegram_payment_charge_id: str
    provider_payment_charge_id: Optional[str] = None
