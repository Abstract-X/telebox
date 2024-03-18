from dataclasses import dataclass
from datetime import datetime

from telebox.bot.types.type import Type
from telebox.bot.types.types.chat_boost_source import ChatBoostSource


@dataclass(repr=False)
class ChatBoost(Type):
    boost_id: str
    add_date: datetime
    expiration_date: datetime
    source: ChatBoostSource
