from attrs import define

from telebox.bot.type import Type


@define(repr=False)
class Invoice(Type):
    title: str
    description: str
    start_parameter: str
    currency: str
    total_amount: int
