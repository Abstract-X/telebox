from dataclasses import dataclass
from typing import Union, Optional

from telebox.bot.types.type import Type
from telebox.bot.types.types.input_file import InputFile
from telebox.bot.consts import input_media_types
from telebox.bot.types.types.message_entity import MessageEntity
from telebox.utils.not_set import NotSet, NOT_SET


@dataclass(repr=False)
class InputMediaPhoto(Type):
    media: Union[InputFile, str]
    caption: Optional[str] = None
    parse_mode: Union[str, None, NotSet] = NOT_SET
    caption_entities: Optional[list[MessageEntity]] = None
    show_caption_above_media: Optional[bool] = None
    has_spoiler: Optional[bool] = None
    type: str = input_media_types.PHOTO
