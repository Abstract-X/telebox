from dataclasses import dataclass
from typing import Optional

from telebox.bot.types.type import Type
from telebox.bot.types.types.user import User
from telebox.bot.types.types.message import Message


@dataclass(eq=False)
class CallbackQuery(Type):
    id: str
    from_: User
    chat_instance: str
    message: Optional[Message] = None
    inline_message_id: Optional[str] = None
    data: Optional[str] = None
    game_short_name: Optional[str] = None

    @property
    def chat_type(self) -> Optional[str]:
        return self.message.chat.type if self.message is not None else None

    @property
    def chat_id(self) -> Optional[int]:
        return self.message.chat.id if self.message is not None else None

    @property
    def user_id(self) -> int:
        return self.from_.id

    @property
    def message_id(self) -> Optional[int]:
        return self.message.message_id if self.message is not None else None
