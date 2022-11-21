from dataclasses import dataclass
from typing import Optional

from telebox.bot.types.type import Type


@dataclass(unsafe_hash=True)
class ForumTopicCreated(Type):
    name: str
    icon_color: int
    icon_custom_emoji_id: Optional[str] = None
