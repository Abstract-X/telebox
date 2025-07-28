from attrs import define

from telebox.bot.type import Type
from telebox.bot.consts import reaction_types


@define(repr=False)
class ReactionTypePaid(Type):
    type: str = reaction_types.PAID
