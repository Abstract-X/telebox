from dataclasses import dataclass
from typing import Optional

from telebox.telegram.types.base import Type
from telebox.telegram.types.types.user import User
from telebox.telegram.types.types.message import Message


@dataclass(unsafe_hash=True)
class CallbackQuery(Type):
    id: str
    from_: User
    chat_instance: str
    message: Optional[Message] = None
    inline_message_id: Optional[str] = None
    data: Optional[str] = None
    game_short_name: Optional[str] = None
