from typing import Union

from telebox.bot.types.types.reaction_type_emoji import ReactionTypeEmoji
from telebox.bot.types.types.reaction_type_custom_emoji import ReactionTypeCustomEmoji
from telebox.bot.types.types.reaction_type_paid import ReactionTypePaid


ReactionType = Union[ReactionTypeEmoji, ReactionTypeCustomEmoji, ReactionTypePaid]
