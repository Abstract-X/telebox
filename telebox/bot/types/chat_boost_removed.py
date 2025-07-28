from datetime import datetime

from attrs import define

from telebox.bot.type import Type
from telebox.bot.types.chat import Chat
from telebox.bot.types.chat_boost_source import ChatBoostSource


@define(repr=False)
class ChatBoostRemoved(Type):
    chat: Chat
    boost_id: str
    remove_date: datetime
    source: ChatBoostSource
