from dataclasses import dataclass

from telebox.bot.types.type import Type
from telebox.bot.consts import withdrawal_state_types


@dataclass(repr=False)
class RevenueWithdrawalStateFailed(Type):
    type: str = withdrawal_state_types.FAILED
