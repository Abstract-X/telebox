from typing import Union

from telebox.bot.types.types.revenue_withdrawal_state_pending import (
    RevenueWithdrawalStatePending
)
from telebox.bot.types.types.revenue_withdrawal_state_succeeded import (
    RevenueWithdrawalStateSucceeded
)
from telebox.bot.types.types.revenue_withdrawal_state_failed import (
    RevenueWithdrawalStateFailed
)


RevenueWithdrawalState = Union[RevenueWithdrawalStatePending,
                               RevenueWithdrawalStateSucceeded,
                               RevenueWithdrawalStateFailed]
