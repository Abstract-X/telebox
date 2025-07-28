from attrs import define

from telebox.bot.type import Type


@define(repr=False)
class ChatBoostAdded(Type):
    boost_count: int
