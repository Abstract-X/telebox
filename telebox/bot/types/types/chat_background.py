from attrs import define

from telebox.bot.types.type import Type
from telebox.bot.types.types.background_type import BackgroundType


@define(repr=False)
class ChatBackground(Type):
    type: BackgroundType
