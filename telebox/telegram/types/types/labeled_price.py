from dataclasses import dataclass

from telebox.telegram.types.base import Type


@dataclass(unsafe_hash=True)
class LabeledPrice(Type):
    label: str
    amount: int
