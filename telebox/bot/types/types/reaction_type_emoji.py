from dataclasses import dataclass

from telebox.bot.types.type import Type


@dataclass
class ReactionTypeEmoji(Type):
    emoji: str
    type: str = "emoji"
