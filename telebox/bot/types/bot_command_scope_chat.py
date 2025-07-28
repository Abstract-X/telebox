from typing import Union

from attrs import define

from telebox.bot.type import Type
from telebox.bot.consts import bot_command_scope_types


@define(repr=False)
class BotCommandScopeChat(Type):
    chat_id: Union[int, str]
    type: str = bot_command_scope_types.CHAT
