from dataclasses import dataclass

from telebox.bot.types.type import Type
from telebox.bot.types.types.labeled_price import LabeledPrice


@dataclass(unsafe_hash=True)
class ShippingOption(Type):
    id: str
    title: str
    prices: list[LabeledPrice]
