from dataclasses import dataclass

from telebox.bot.types.type import Type
from telebox.bot.types.types.reaction_type import ReactionType


@dataclass(repr=False)
class ReactionCount(Type):
    type: ReactionType
    total_count: int
