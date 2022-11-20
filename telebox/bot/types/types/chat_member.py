from typing import Union

from telebox.bot.types.types.chat_member_owner import ChatMemberOwner
from telebox.bot.types.types.chat_member_administrator import ChatMemberAdministrator
from telebox.bot.types.types.chat_member_member import ChatMemberMember
from telebox.bot.types.types.chat_member_restricted import ChatMemberRestricted
from telebox.bot.types.types.chat_member_left import ChatMemberLeft
from telebox.bot.types.types.chat_member_banned import ChatMemberBanned


ChatMember = Union[ChatMemberOwner,
                   ChatMemberAdministrator,
                   ChatMemberMember,
                   ChatMemberRestricted,
                   ChatMemberLeft,
                   ChatMemberBanned]
