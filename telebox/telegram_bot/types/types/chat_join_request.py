from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from telebox.telegram_bot.types.type import Type
from telebox.telegram_bot.types.types.chat import Chat
from telebox.telegram_bot.types.types.user import User
from telebox.telegram_bot.types.types.chat_invite_link import ChatInviteLink


@dataclass(unsafe_hash=True)
class ChatJoinRequest(Type):
    chat: Chat
    from_: User
    date: datetime
    bio: Optional[str] = None
    invite_link: Optional[ChatInviteLink] = None

    @property
    def chat_type(self) -> str:
        return self.chat.type

    @property
    def chat_id(self) -> int:
        return self.chat.id

    @property
    def user_id(self) -> int:
        return self.from_.id
