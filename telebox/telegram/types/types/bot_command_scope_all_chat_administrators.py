from dataclasses import dataclass

from telebox.telegram.types.base import Type
from telebox.telegram.consts import bot_command_scope_types


@dataclass(unsafe_hash=True)
class BotCommandScopeAllChatAdministrators(Type):
    type: str = bot_command_scope_types.ALL_CHAT_ADMINISTRATORS
