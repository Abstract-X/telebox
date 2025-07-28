from typing import Literal, Optional

from attrs import define

from telebox.bot.type import Type


@define(repr=False)
class ForceReply(Type):
    force_reply: Literal[True] = True
    input_field_placeholder: Optional[str] = None
    selective: Optional[bool] = None
