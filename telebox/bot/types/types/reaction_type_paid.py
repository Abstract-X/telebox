from dataclasses import dataclass

from telebox.bot.types.type import Type
from telebox.bot.consts import reaction_types


@dataclass(repr=False)
class ReactionTypePaid(Type):
    type: str = reaction_types.PAID
