from typing import Union

from telebox.bot.types.types.background_type_fill import BackgroundTypeFill
from telebox.bot.types.types.background_type_wallpaper import BackgroundTypeWallpaper
from telebox.bot.types.types.background_type_pattern import BackgroundTypePattern
from telebox.bot.types.types.background_type_chat_theme import BackgroundTypeChatTheme


BackgroundType = Union[BackgroundTypeFill,
                       BackgroundTypeWallpaper,
                       BackgroundTypePattern,
                       BackgroundTypeChatTheme]
