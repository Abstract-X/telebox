from typing import Optional

from attrs import define

from telebox.bot.type import Type
from telebox.bot.consts import transaction_partner_types
from telebox.bot.types.revenue_withdrawal_state import RevenueWithdrawalState


@define(repr=False)
class TransactionPartnerFragment(Type):
    withdrawal_state: Optional[RevenueWithdrawalState] = None
    type: str = transaction_partner_types.FRAGMENT
