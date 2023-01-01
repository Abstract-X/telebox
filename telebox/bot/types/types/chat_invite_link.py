from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from telebox.bot.types.type import Type
from telebox.bot.types.types.user import User


@dataclass(eq=False)
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
