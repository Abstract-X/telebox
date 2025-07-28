from attrs import define

from telebox.bot.type import Type
from telebox.bot.consts import reaction_types


@define(repr=False)
class ReactionTypeCustomEmoji(Type):
    custom_emoji_id: str
    type: str = reaction_types.CUSTOM_EMOJI
