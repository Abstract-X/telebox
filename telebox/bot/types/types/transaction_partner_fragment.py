from dataclasses import dataclass
from typing import Optional

from telebox.bot.types.type import Type
from telebox.bot.consts import transaction_partner_types
from telebox.bot.types.types.revenue_withdrawal_state import RevenueWithdrawalState


@dataclass(repr=False)
class TransactionPartnerFragment(Type):
    withdrawal_state: Optional[RevenueWithdrawalState] = None
    type: str = transaction_partner_types.FRAGMENT
