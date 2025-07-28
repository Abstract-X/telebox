from typing import Optional

from attrs import define

from telebox.bot.type import Type
from telebox.bot.types.chat import Chat
from telebox.bot.types.user import User


@define(repr=False)
class PollAnswer(Type):
    poll_id: str
    option_ids: list[int]
    voter_chat: Optional[Chat] = None
    user: Optional[User] = None

    @property
    def voter_chat_id(self) -> Optional[int]:
        if self.voter_chat is not None:
            return self.voter_chat.id

    @property
    def user_id(self) -> Optional[int]:
        if self.user is not None:
            return self.user.id
