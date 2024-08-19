from dataclasses import dataclass

from telebox.bot.types.type import Type
from telebox.bot.consts import reaction_types


@dataclass(repr=False)
class ReactionTypeCustomEmoji(Type):
    custom_emoji_id: str
    type: str = reaction_types.CUSTOM_EMOJI
