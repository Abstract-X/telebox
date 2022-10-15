from dataclasses import dataclass
from typing import Optional

from telebox.telegram_bot.types.type import Type
from telebox.telegram_bot.consts import chat_member_statuses
from telebox.telegram_bot.types.types.user import User


@dataclass(unsafe_hash=True)
class ChatMemberAdministrator(Type):
    user: User
    can_be_edited: bool
    is_anonymous: bool
    can_manage_chat: bool
    can_delete_messages: bool
    can_manage_video_chats: bool
    can_restrict_members: bool
    can_promote_members: bool
    can_change_info: bool
    can_invite_users: bool
    can_post_messages: Optional[bool] = None
    can_edit_messages: Optional[bool] = None
    can_pin_messages: Optional[bool] = None
    custom_title: Optional[str] = None
    status: str = chat_member_statuses.ADMINISTRATOR
