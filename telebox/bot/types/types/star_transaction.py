from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from telebox.bot.types.type import Type
from telebox.bot.types.types.transaction_partner import TransactionPartner


@dataclass(repr=False)
class StarTransaction(Type):
    id: str
    amount: int
    date: datetime
    source: Optional[TransactionPartner] = None
    receiver: Optional[TransactionPartner] = None
