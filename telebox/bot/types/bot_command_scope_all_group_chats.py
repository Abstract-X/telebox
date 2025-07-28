from attrs import define

from telebox.bot.type import Type
from telebox.bot.consts import bot_command_scope_types


@define(repr=False)
class BotCommandScopeAllGroupChats(Type):
    type: str = bot_command_scope_types.ALL_GROUP_CHATS
