from dataclasses import dataclass
from typing import Optional

from telebox.bot.types.type import Type
from telebox.bot.types.types.chat_administrator_rights import ChatAdministratorRights


@dataclass
class KeyboardButtonRequestChat(Type):
    request_id: int
    chat_is_channel: bool
    chat_is_forum: Optional[bool] = None
    chat_has_username: Optional[bool] = None
    chat_is_created: Optional[bool] = None
    user_administrator_rights: Optional[ChatAdministratorRights] = None
    bot_administrator_rights: Optional[ChatAdministratorRights] = None
    bot_is_member: Optional[bool] = None
