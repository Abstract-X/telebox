from dataclasses import dataclass

from telebox.bot.types.type import Type
from telebox.bot.types.types.chat import Chat
from telebox.bot.types.types.chat_boost import ChatBoost


@dataclass
class ChatBoostUpdated(Type):
    chat: Chat
    boost: ChatBoost
