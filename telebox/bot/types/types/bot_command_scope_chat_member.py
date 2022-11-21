from dataclasses import dataclass
from typing import Union

from telebox.bot.types.type import Type
from telebox.bot.consts import bot_command_scope_types


@dataclass(unsafe_hash=True)
class BotCommandScopeChatMember(Type):
    chat_id: Union[int, str]
    user_id: int
    type: str = bot_command_scope_types.CHAT_MEMBER
