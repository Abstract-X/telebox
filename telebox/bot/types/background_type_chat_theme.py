from attrs import define

from telebox.bot.type import Type
from telebox.bot.consts import background_types


@define(repr=False)
class BackgroundTypeChatTheme(Type):
    theme_name: str
    type: str = background_types.CHAT_THEME
