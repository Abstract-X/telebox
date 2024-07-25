from dataclasses import dataclass
from datetime import datetime

from telebox.bot.types.type import Type
from telebox.bot.consts import withdrawal_state_types


@dataclass(repr=False)
class RevenueWithdrawalStateSucceeded(Type):
    date: datetime
    url: str
    type: str = withdrawal_state_types.SUCCEEDED
