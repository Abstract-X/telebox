from attrs import define

from telebox.bot.types.type import Type
from telebox.bot.types.types.star_transaction import StarTransaction


@define(repr=False)
class StarTransactions(Type):
    transactions: list[StarTransaction]
