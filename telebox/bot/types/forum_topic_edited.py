from typing import Optional

from attrs import define

from telebox.bot.type import Type


@define(repr=False)
class ForumTopicEdited(Type):
    name: Optional[str] = None
    icon_custom_emoji_id: Optional[str] = None
