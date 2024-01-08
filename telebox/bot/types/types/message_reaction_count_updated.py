from datetime import datetime
from dataclasses import dataclass

from telebox.bot.utils.ids import get_unprefixed_chat_id
from telebox.bot.types.type import Type
from telebox.bot.types.types.chat import Chat
from telebox.bot.types.types.reaction_count import ReactionCount


@dataclass
class MessageReactionCountUpdated(Type):
    chat: Chat
    message_id: int
    date: datetime
    reactions: list[ReactionCount]

    @property
    def chat_type(self) -> str:
        return self.chat.type

    @property
    def chat_id(self) -> int:
        return self.chat.id

    @property
    def unprefixed_chat_id(self) -> int:
        return get_unprefixed_chat_id(self.chat_id, self.chat_type)
