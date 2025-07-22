from attrs import define

from telebox.bot.types.type import Type
from telebox.bot.consts import withdrawal_state_types


@define(repr=False)
class RevenueWithdrawalStateFailed(Type):
    type: str = withdrawal_state_types.FAILED
