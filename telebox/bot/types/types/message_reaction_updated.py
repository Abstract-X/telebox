from typing import Optional
from datetime import datetime
from dataclasses import dataclass

from telebox.bot.utils.ids import get_unprefixed_chat_id
from telebox.bot.types.type import Type
from telebox.bot.types.types.chat import Chat
from telebox.bot.types.types.user import User
from telebox.bot.types.types.reaction_type import ReactionType


@dataclass
class MessageReactionUpdated(Type):
    chat: Chat
    message_id: int
    date: datetime
    old_reaction: list[ReactionType]
    new_reaction: list[ReactionType]
    user: Optional[User] = None
    actor_chat: Optional[User] = None

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
    def user_id(self) -> Optional[int]:
        return self.user.id if self.user is not None else None
