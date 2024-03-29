from dataclasses import dataclass

from telebox.bot.types.type import Type


@dataclass(repr=False)
class Invoice(Type):
    title: str
    description: str
    start_parameter: str
    currency: str
    total_amount: int
