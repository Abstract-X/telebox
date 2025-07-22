from typing import Optional

from attrs import define

from telebox.bot.types.type import Type
from telebox.bot.types.types.user import User
from telebox.bot.types.types.location import Location


@define(repr=False)
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
