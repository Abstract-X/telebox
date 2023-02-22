from dataclasses import dataclass
from typing import Optional

from telebox.bot.types.type import Type


@dataclass
class ResponseParameters(Type):
    migrate_to_chat_id: Optional[int] = None
    retry_after: Optional[int] = None
