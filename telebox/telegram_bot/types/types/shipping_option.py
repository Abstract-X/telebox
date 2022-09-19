from dataclasses import dataclass

from telebox.telegram_bot.types.base import Type
from telebox.telegram_bot.types.types.labeled_price import LabeledPrice


@dataclass(unsafe_hash=True)
class ShippingOption(Type):
    id: str
    title: str
    prices: list[LabeledPrice]
