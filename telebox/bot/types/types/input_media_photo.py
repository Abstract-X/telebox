from dataclasses import dataclass
from typing import Union, Optional

from telebox.bot.types.type import Type
from telebox.bot.types.types.input_file import InputFile
from telebox.bot.consts import input_media_types
from telebox.bot.types.types.message_entity import MessageEntity


@dataclass
class InputMediaPhoto(Type):
    media: Union[InputFile, str]
    caption: Optional[str] = None
    parse_mode: Optional[str] = None
    caption_entities: Optional[list[MessageEntity]] = None
    has_spoiler: Optional[bool] = None
    type: str = input_media_types.PHOTO
