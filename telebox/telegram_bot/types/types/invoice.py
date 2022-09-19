from dataclasses import dataclass

from telebox.telegram_bot.types.base import Type


@dataclass(unsafe_hash=True)
class Invoice(Type):
    title: str
    description: str
    start_parameter: str
    currency: str
    total_amount: int
