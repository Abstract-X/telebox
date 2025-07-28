from attrs import define

from telebox.bot.type import Type
from telebox.bot.types.reaction_type import ReactionType


@define(repr=False)
class ReactionCount(Type):
    type: ReactionType
    total_count: int
