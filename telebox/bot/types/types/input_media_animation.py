from dataclasses import dataclass
from typing import Union, Optional

from telebox.bot.types.type import Type
from telebox.bot.consts import input_media_types
from telebox.bot.types.types.input_file import InputFile
from telebox.bot.types.types.message_entity import MessageEntity


@dataclass(repr=False)
class InputMediaAnimation(Type):
    media: Union[InputFile, str]
    thumbnail: Union[InputFile, str, None] = None
    caption: Optional[str] = None
    parse_mode: Optional[str] = None
    caption_entities: Optional[list[MessageEntity]] = None
    show_caption_above_media: Optional[bool] = None
    width: Optional[int] = None
    height: Optional[int] = None
    duration: Optional[int] = None
    has_spoiler: Optional[bool] = None
    type: str = input_media_types.ANIMATION
