from dataclasses import dataclass
from typing import Optional

from telebox.bot.types.type import Type
from telebox.bot.consts import transaction_partner_types
from telebox.bot.types.types.user import User


@dataclass(repr=False)
class TransactionPartnerUser(Type):
    user: User
    invoice_payload: Optional[str] = None
    type: str = transaction_partner_types.USER
