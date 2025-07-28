from typing import Optional

from attrs import define

from telebox.bot.type import Type


@define(repr=False)
class SentWebAppMessage(Type):
    inline_message_id: Optional[str] = None
