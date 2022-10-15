from dataclasses import dataclass
from typing import Literal, Optional

from telebox.telegram_bot.types.type import Type


@dataclass(unsafe_hash=True)
class ForceReply(Type):
    force_reply: Literal[True] = True
    input_field_placeholder: Optional[str] = None
    selective: Optional[bool] = None
