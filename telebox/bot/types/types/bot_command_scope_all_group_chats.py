from dataclasses import dataclass

from telebox.bot.types.type import Type
from telebox.bot.consts import bot_command_scope_types


@dataclass(repr=False)
class BotCommandScopeAllGroupChats(Type):
    type: str = bot_command_scope_types.ALL_GROUP_CHATS
