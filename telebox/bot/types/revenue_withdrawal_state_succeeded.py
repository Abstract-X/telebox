from datetime import datetime

from attrs import define

from telebox.bot.type import Type
from telebox.bot.consts import withdrawal_state_types


@define(repr=False)
class RevenueWithdrawalStateSucceeded(Type):
    date: datetime
    url: str
    type: str = withdrawal_state_types.SUCCEEDED
