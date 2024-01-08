from dataclasses import dataclass
from datetime import datetime

from telebox.bot.types.type import Type
from telebox.bot.types.types.chat import Chat
from telebox.bot.types.types.chat_boost_source import ChatBoostSource


@dataclass
class ChatBoostRemoved(Type):
    chat: Chat
    boost_id: str
    remove_date: datetime
    source: ChatBoostSource
