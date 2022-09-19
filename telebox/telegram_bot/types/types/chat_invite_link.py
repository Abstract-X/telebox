from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from telebox.telegram_bot.types.base import Type
from telebox.telegram_bot.types.types.user import User


@dataclass(unsafe_hash=True)
class ChatInviteLink(Type):
    invite_link: str
    creator: User
    creates_join_request: bool
    is_primary: bool
    is_revoked: bool
    name: Optional[str] = None
    expire_date: Optional[datetime] = None
    member_limit: Optional[int] = None
    pending_join_request_count: Optional[int] = None
