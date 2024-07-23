from dataclasses import dataclass

from telebox.bot.types.type import Type
from telebox.bot.types.types.star_transaction import StarTransaction


@dataclass(repr=False)
class StarTransactions(Type):
    transactions: list[StarTransaction]
