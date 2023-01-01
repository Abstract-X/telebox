from dataclasses import dataclass

from telebox.bot.types.type import Type


@dataclass(eq=False)
class LabeledPrice(Type):
    label: str
    amount: int
