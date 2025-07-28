from attrs import define

from telebox.bot.type import Type
from telebox.bot.types.chat import Chat


@define(repr=False)
class Story(Type):
    chat: Chat
    id: int
