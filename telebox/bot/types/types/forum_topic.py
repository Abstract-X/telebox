from dataclasses import dataclass
from typing import Optional

from telebox.bot.types.type import Type


@dataclass(unsafe_hash=True)
class ForumTopic(Type):
    message_thread_id: int
    name: str
    icon_color: int
    icon_custom_emoji_id: Optional[str] = None
