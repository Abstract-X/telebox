from typing import Union

from telebox.bot.types.types.message_origin_user import MessageOriginUser
from telebox.bot.types.types.message_origin_hidden_user import MessageOriginHiddenUser
from telebox.bot.types.types.message_origin_chat import MessageOriginChat
from telebox.bot.types.types.message_origin_channel import MessageOriginChannel


MessageOrigin = Union[MessageOriginUser,
                      MessageOriginHiddenUser,
                      MessageOriginChat,
                      MessageOriginChannel]
