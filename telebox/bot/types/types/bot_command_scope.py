from typing import Union

from telebox.bot.types.types.bot_command_scope_default import (
    BotCommandScopeDefault
)
from telebox.bot.types.types.bot_command_scope_all_private_chats import (
    BotCommandScopeAllPrivateChats
)
from telebox.bot.types.types.bot_command_scope_all_group_chats import (
    BotCommandScopeAllGroupChats
)
from telebox.bot.types.types.bot_command_scope_all_chat_administrators import (
    BotCommandScopeAllChatAdministrators
)
from telebox.bot.types.types.bot_command_scope_chat import (
    BotCommandScopeChat
)
from telebox.bot.types.types.bot_command_scope_chat_administrators import (
    BotCommandScopeChatAdministrators
)
from telebox.bot.types.types.bot_command_scope_chat_member import (
    BotCommandScopeChatMember
)


BotCommandScope = Union[BotCommandScopeDefault,
                        BotCommandScopeAllPrivateChats,
                        BotCommandScopeAllGroupChats,
                        BotCommandScopeAllChatAdministrators,
                        BotCommandScopeChat,
                        BotCommandScopeChatAdministrators,
                        BotCommandScopeChatMember]
