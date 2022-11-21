from dataclasses import dataclass

from telebox.bot.types.type import Type


@dataclass(unsafe_hash=True)
class LabeledPrice(Type):
    label: str
    amount: int
