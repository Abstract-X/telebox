from dataclasses import dataclass

from telebox.bot.types.type import Type


@dataclass(repr=False)
class ReactionTypeEmoji(Type):
    emoji: str
    type: str = "emoji"
