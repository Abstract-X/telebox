from typing import Optional

from attrs import define

from telebox.bot.type import Type
from telebox.bot.consts import transaction_partner_types
from telebox.bot.types.user import User
from telebox.bot.types.paid_media import PaidMedia


@define(repr=False)
class TransactionPartnerUser(Type):
    user: User
    invoice_payload: Optional[str] = None
    type: str = transaction_partner_types.USER
    paid_media: Optional[PaidMedia] = None
