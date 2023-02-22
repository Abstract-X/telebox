from dataclasses import dataclass
from typing import Optional

from telebox.bot.types.type import Type
from telebox.bot.consts import input_media_types
from telebox.bot.types.types.message_entity import MessageEntity


@dataclass
class InputMediaPhoto(Type):
    media: str
    caption: Optional[str] = None
    parse_mode: Optional[str] = None
    caption_entities: Optional[list[MessageEntity]] = None
    type: str = input_media_types.PHOTO
