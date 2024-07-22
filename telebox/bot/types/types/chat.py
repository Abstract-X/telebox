from dataclasses import dataclass
from typing import Literal, Optional

from telebox.bot.types.type import Type
from telebox.bot.utils.users import get_full_name
from telebox.bot.utils.deep_links import get_username_link


@dataclass(repr=False)
class Chat(Type):
    id: int
    type: str
    title: Optional[str] = None
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_forum: Optional[Literal[True]] = None

    @property
    def full_name(self) -> Optional[str]:
        if self.first_name is not None:
            return get_full_name(self.first_name, self.last_name)

    @property
    def link(self) -> Optional[str]:
        if self.username is not None:
            return get_username_link(self.username)
