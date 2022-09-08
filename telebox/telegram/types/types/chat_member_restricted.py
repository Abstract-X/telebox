from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from telebox.telegram.types.base import Type
from telebox.telegram.consts import chat_member_statuses
from telebox.telegram.types.types.user import User


@dataclass(unsafe_hash=True)
class ChatMemberRestricted(Type):
    user: User
    is_member: bool
    can_change_info: bool
    can_invite_users: bool
    can_pin_messages: bool
    can_send_messages: bool
    can_send_media_messages: bool
    can_send_polls: bool
    can_send_other_messages: bool
    can_add_web_page_previews: bool
    until_date: Optional[datetime] = None  # None instead of 0
    status: str = chat_member_statuses.RESTRICTED
