from dataclasses import dataclass

from telebox.bot.types.type import Type
from telebox.bot.consts import bot_command_scope_types


@dataclass(eq=False)
class BotCommandScopeAllPrivateChats(Type):
    type: str = bot_command_scope_types.ALL_PRIVATE_CHATS
