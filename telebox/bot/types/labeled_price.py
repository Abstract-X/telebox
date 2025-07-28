from attrs import define

from telebox.bot.type import Type


@define(repr=False)
class LabeledPrice(Type):
    label: str
    amount: int
