from attrs import define

from telebox.bot.type import Type
from telebox.bot.types.chat import Chat
from telebox.bot.types.chat_boost import ChatBoost


@define(repr=False)
class ChatBoostUpdated(Type):
    chat: Chat
    boost: ChatBoost
