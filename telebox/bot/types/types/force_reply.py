from dataclasses import dataclass
from typing import Literal, Optional

from telebox.bot.types.type import Type


@dataclass(eq=False)
class ForceReply(Type):
    force_reply: Literal[True] = True
    input_field_placeholder: Optional[str] = None
    selective: Optional[bool] = None
