from attrs import define

from telebox.bot.types.type import Type
from telebox.bot.types.types.chat import Chat
from telebox.bot.types.types.chat_boost import ChatBoost


@define(repr=False)
class ChatBoostUpdated(Type):
    chat: Chat
    boost: ChatBoost
