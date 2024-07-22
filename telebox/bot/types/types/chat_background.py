from dataclasses import dataclass

from telebox.bot.types.type import Type
from telebox.bot.types.types.background_type import BackgroundType


@dataclass(repr=False)
class ChatBackground(Type):
    type: BackgroundType
