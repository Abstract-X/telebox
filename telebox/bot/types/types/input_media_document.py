from dataclasses import dataclass
from typing import Union, Optional

from telebox.bot.types.type import Type
from telebox.bot.consts import input_media_types
from telebox.bot.types.types.input_file import InputFile
from telebox.bot.types.types.message_entity import MessageEntity
from telebox.utils.not_set import NotSet, NOT_SET


@dataclass(repr=False)
class InputMediaDocument(Type):
    media: Union[InputFile, str]
    thumbnail: Union[InputFile, str, None] = None
    caption: Optional[str] = None
    parse_mode: Union[str, None, NotSet] = NOT_SET
    caption_entities: Optional[list[MessageEntity]] = None
    disable_content_type_detection: Optional[bool] = None
    type: str = input_media_types.DOCUMENT
