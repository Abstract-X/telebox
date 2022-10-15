from dataclasses import dataclass
from typing import Optional

from telebox.telegram_bot.types.type import Type
from telebox.telegram_bot.types.types.user import User
from telebox.telegram_bot.types.types.location import Location


@dataclass(unsafe_hash=True)
class InlineQuery(Type):
    id: str
    from_: User
    query: str
    offset: str
    chat_type: Optional[str] = None
    location: Optional[Location] = None

    @property
    def user_id(self) -> int:
        return self.from_.id
