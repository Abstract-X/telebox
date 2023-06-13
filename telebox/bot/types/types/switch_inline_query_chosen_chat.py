from dataclasses import dataclass
from typing import Optional

from telebox.bot.types.type import Type


@dataclass
class SwitchInlineQueryChosenChat(Type):
    query: Optional[str] = None
    allow_user_chats: Optional[bool] = None
    allow_bot_chats: Optional[bool] = None
    allow_group_chats: Optional[bool] = None
    allow_channel_chats: Optional[bool] = None
