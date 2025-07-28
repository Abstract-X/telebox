from attrs import define

from telebox.bot.type import Type
from telebox.bot.types.labeled_price import LabeledPrice


@define(repr=False)
class ShippingOption(Type):
    id: str
    title: str
    prices: list[LabeledPrice]
