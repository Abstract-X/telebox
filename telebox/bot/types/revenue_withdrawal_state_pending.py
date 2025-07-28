from attrs import define

from telebox.bot.type import Type
from telebox.bot.consts import withdrawal_state_types


@define(repr=False)
class RevenueWithdrawalStatePending(Type):
    type: str = withdrawal_state_types.PENDING
