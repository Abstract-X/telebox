from typing import Optional

from attrs import define

from telebox.bot.types.type import Type


@define(repr=False)
class ForumTopic(Type):
    message_thread_id: int
    name: str
    icon_color: int
    icon_custom_emoji_id: Optional[str] = None
