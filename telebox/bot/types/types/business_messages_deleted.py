from attrs import define

from telebox.bot.types.type import Type
from telebox.bot.types.types.chat import Chat


@define(repr=False)
class BusinessMessagesDeleted(Type):
    business_connection_id: str
    chat: Chat
    message_ids: list[int]
