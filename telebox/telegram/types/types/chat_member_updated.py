from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from telebox.telegram.types.base import Type
from telebox.telegram.types.types.chat import Chat
from telebox.telegram.types.types.user import User
from telebox.telegram.types.types.chat_member import ChatMember
from telebox.telegram.types.types.chat_invite_link import ChatInviteLink


@dataclass(unsafe_hash=True)
class ChatMemberUpdated(Type):
    chat: Chat
    from_: User
    date: datetime
    old_chat_member: ChatMember
    new_chat_member: ChatMember
    invite_link: Optional[ChatInviteLink] = None
