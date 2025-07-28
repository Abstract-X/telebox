from attrs import define

from telebox.bot.type import Type
from telebox.bot.types.background_type import BackgroundType


@define(repr=False)
class ChatBackground(Type):
    type: BackgroundType
