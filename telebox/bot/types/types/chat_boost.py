from dataclasses import dataclass
from datetime import datetime

from telebox.bot.types.type import Type
from telebox.bot.types.types.chat_boost_source import ChatBoostSource


@dataclass
class ChatBoost(Type):
    boost_id: int
    add_date: datetime
    expiration_date: datetime
    source: ChatBoostSource
