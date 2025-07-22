from attrs import define

from telebox.bot.types.type import Type
from telebox.bot.consts import reaction_types


@define(repr=False)
class ReactionTypeEmoji(Type):
    emoji: str
    type: str = reaction_types.EMOJI
