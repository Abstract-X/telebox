from dataclasses import dataclass
from typing import Optional, Literal

from telebox.telegram_bot.types.type import Type
from telebox.telegram_bot.utils import get_url, get_user_mention_url, get_full_name


@dataclass(unsafe_hash=True)
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
    def url(self) -> Optional[str]:
        if self.username is not None:
            return get_url(self.username)

    @property
    def mention_url(self) -> str:
        return get_user_mention_url(self.id)
