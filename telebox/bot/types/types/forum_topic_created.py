from typing import Optional

from attrs import define

from telebox.bot.types.type import Type


@define(repr=False)
class ForumTopicCreated(Type):
    name: str
    icon_color: int
    icon_custom_emoji_id: Optional[str] = None
