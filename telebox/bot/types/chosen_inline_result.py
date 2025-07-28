from typing import Optional

from attrs import define

from telebox.bot.type import Type
from telebox.bot.types.user import User
from telebox.bot.types.location import Location


@define(repr=False)
class ChosenInlineResult(Type):
    result_id: str
    from_: User
    query: str
    location: Optional[Location] = None
    inline_message_id: Optional[str] = None

    @property
    def user_id(self) -> int:
        return self.from_.id
