from dataclasses import dataclass
from typing import Optional, Literal

from telebox.bot.types.type import Type
from telebox.bot.utils.users import get_full_name
from telebox.bot.utils.deep_links import get_username_link, get_user_link


@dataclass(repr=False)
class WebAppUser(Type):
    id: int
    first_name: str
    last_name: Optional[str] = None
    username: Optional[str] = None
    is_bot: Optional[bool] = None
    language_code: Optional[str] = None
    is_premium: Optional[Literal[True]] = None
    added_to_attachment_menu: Optional[Literal[True]] = None
    allows_write_to_pm: Optional[Literal[True]] = None
    photo_url: Optional[str] = None

    @property
    def full_name(self) -> str:
        return get_full_name(first_name=self.first_name, last_name=self.last_name)

    @property
    def link(self) -> Optional[str]:
        if self.username:
            return get_username_link(self.username)

    @property
    def mention_link(self) -> str:
        return get_user_link(self.id)
