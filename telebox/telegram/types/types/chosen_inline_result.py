from dataclasses import dataclass
from typing import Optional

from telebox.telegram.types.base import Type
from telebox.telegram.types.types.user import User
from telebox.telegram.types.types.location import Location


@dataclass(unsafe_hash=True)
class ChosenInlineResult(Type):
    result_id: str
    from_: User
    query: str
    location: Optional[Location] = None
    inline_message_id: Optional[str] = None
