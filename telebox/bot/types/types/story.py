from dataclasses import dataclass

from telebox.bot.types.type import Type
from telebox.bot.types.types.chat import Chat


@dataclass(repr=False)
class Story(Type):
    chat: Chat
    id: int
