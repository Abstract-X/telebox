from dataclasses import dataclass

from telebox.bot.types.type import Type


@dataclass(repr=False)
class ChatBoostAdded(Type):
    boost_count: int
