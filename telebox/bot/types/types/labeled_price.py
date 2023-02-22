from dataclasses import dataclass

from telebox.bot.types.type import Type


@dataclass
class LabeledPrice(Type):
    label: str
    amount: int
