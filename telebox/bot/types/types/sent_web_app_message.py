from dataclasses import dataclass
from typing import Optional

from telebox.bot.types.type import Type


@dataclass(eq=False)
class SentWebAppMessage(Type):
    inline_message_id: Optional[str] = None
