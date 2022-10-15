from dataclasses import dataclass

from telebox.telegram_bot.types.type import Type
from telebox.telegram_bot.consts import bot_command_scope_types


@dataclass(unsafe_hash=True)
class BotCommandScopeAllPrivateChats(Type):
    type: str = bot_command_scope_types.ALL_PRIVATE_CHATS
