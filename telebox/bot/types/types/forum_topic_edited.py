from dataclasses import dataclass
from typing import Optional

from telebox.bot.types.type import Type


@dataclass(repr=False)
class ForumTopicEdited(Type):
    name: Optional[str] = None
    icon_custom_emoji_id: Optional[str] = None
