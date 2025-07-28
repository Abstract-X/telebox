from attrs import define

from telebox.bot.type import Type
from telebox.bot.types.star_transaction import StarTransaction


@define(repr=False)
class StarTransactions(Type):
    transactions: list[StarTransaction]
