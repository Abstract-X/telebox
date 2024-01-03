from typing import Union

from telebox.bot.types.types.reaction_type_emoji import ReactionTypeEmoji
from telebox.bot.types.types.reaction_type_custom_emoji import ReactionTypeCustomEmoji


ReactionType = Union[ReactionTypeEmoji, ReactionTypeCustomEmoji]
