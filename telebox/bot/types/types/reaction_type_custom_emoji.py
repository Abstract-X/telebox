from dataclasses import dataclass

from telebox.bot.types.type import Type


@dataclass(repr=False)
class ReactionTypeCustomEmoji(Type):
    custom_emoji_id: str
    type: str = "custom_emoji"
