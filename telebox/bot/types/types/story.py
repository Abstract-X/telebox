from attrs import define

from telebox.bot.types.type import Type
from telebox.bot.types.types.chat import Chat


@define(repr=False)
class Story(Type):
    chat: Chat
    id: int
