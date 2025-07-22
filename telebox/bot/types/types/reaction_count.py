from attrs import define

from telebox.bot.types.type import Type
from telebox.bot.types.types.reaction_type import ReactionType


@define(repr=False)
class ReactionCount(Type):
    type: ReactionType
    total_count: int
