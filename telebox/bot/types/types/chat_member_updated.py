from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from telebox.bot.types.type import Type
from telebox.bot.types.types.chat import Chat
from telebox.bot.types.types.user import User
from telebox.bot.types.types.chat_member import ChatMember
from telebox.bot.types.types.chat_invite_link import ChatInviteLink
from telebox.bot.utils.ids import get_unprefixed_chat_id


@dataclass
class ChatMemberUpdated(Type):
    chat: Chat
    from_: User
    date: datetime
    old_chat_member: ChatMember
    new_chat_member: ChatMember
    invite_link: Optional[ChatInviteLink] = None
    via_chat_folder_invite_link: Optional[bool] = None

    @property
    def chat_type(self) -> str:
        return self.chat.type

    @property
    def chat_id(self) -> int:
        return self.chat.id

    @property
    def unprefixed_chat_id(self) -> int:
        return get_unprefixed_chat_id(self.chat_id, self.chat_type)

    @property
    def user_id(self) -> int:
        return self.from_.id
