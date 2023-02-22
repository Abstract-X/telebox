from dataclasses import dataclass
from typing import Optional, Literal

from telebox.bot.types.type import Type
from telebox.bot.utils.users import get_full_name
from telebox.bot.utils.deep_links import get_username_link, get_user_link


@dataclass
class User(Type):
    id: int
    is_bot: bool
    first_name: str
    last_name: Optional[str] = None
    username: Optional[str] = None
    language_code: Optional[str] = None
    is_premium: Optional[Literal[True]] = None
    added_to_attachment_menu: Optional[Literal[True]] = None
    can_join_groups: Optional[bool] = None
    can_read_all_group_messages: Optional[bool] = None
    supports_inline_queries: Optional[bool] = None

    @property
    def full_name(self) -> str:
        return get_full_name(self.first_name, self.last_name)

    @property
    def link(self) -> Optional[str]:
        if self.username is not None:
            return get_username_link(self.username)

    @property
    def mention_link(self) -> str:
        return get_user_link(self.id)
