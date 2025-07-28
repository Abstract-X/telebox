from datetime import datetime

from attrs import define

from telebox.bot.type import Type
from telebox.bot.types.chat_boost_source import ChatBoostSource


@define(repr=False)
class ChatBoost(Type):
    boost_id: str
    add_date: datetime
    expiration_date: datetime
    source: ChatBoostSource
