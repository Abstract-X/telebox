from dataclasses import dataclass
from typing import Optional

from telebox.telegram.types.base import Type
from telebox.telegram.consts import input_media_types
from telebox.telegram.types.types.message_entity import MessageEntity


@dataclass(unsafe_hash=True)
class InputMediaPhoto(Type):
    media: str
    caption: Optional[str] = None
    parse_mode: Optional[str] = None
    caption_entities: Optional[list[MessageEntity]] = None
    type: str = input_media_types.PHOTO
