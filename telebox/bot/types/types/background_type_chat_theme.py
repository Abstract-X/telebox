from dataclasses import dataclass

from telebox.bot.types.type import Type
from telebox.bot.consts import background_types


@dataclass(repr=False)
class BackgroundTypeChatTheme(Type):
    theme_name: str
    type: str = background_types.CHAT_THEME
