from dataclasses import dataclass
from typing import Union

from telebox.bot.types.type import Type
from telebox.bot.consts import bot_command_scope_types


@dataclass
class BotCommandScopeChat(Type):
    chat_id: Union[int, str]
    type: str = bot_command_scope_types.CHAT
