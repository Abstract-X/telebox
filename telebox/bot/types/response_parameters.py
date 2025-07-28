from typing import Optional

from attrs import define

from telebox.bot.type import Type


@define(repr=False)
class ResponseParameters(Type):
    migrate_to_chat_id: Optional[int] = None
    retry_after: Optional[int] = None
