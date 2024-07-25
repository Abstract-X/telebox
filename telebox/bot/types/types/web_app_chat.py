from dataclasses import dataclass
from typing import Optional

from telebox.bot.types.type import Type
from telebox.bot.utils.deep_links import get_username_link


@dataclass(repr=False)
class WebAppChat(Type):
    id: int
    type: str
    title: str
    username: Optional[str] = None
    photo_url: Optional[str] = None

    @property
    def link(self) -> Optional[str]:
        if self.username:
            return get_username_link(self.username)
