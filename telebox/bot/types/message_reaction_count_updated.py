from datetime import datetime

from attrs import define

from telebox.bot.utils.ids import get_unprefixed_chat_id
from telebox.bot.type import Type
from telebox.bot.types.chat import Chat
from telebox.bot.types.reaction_count import ReactionCount


@define(repr=False)
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
