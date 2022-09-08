from dataclasses import dataclass
from typing import Optional

from telebox.telegram.types.base import Type


@dataclass(unsafe_hash=True)
class SentWebAppMessage(Type):
    inline_message_id: Optional[str] = None
