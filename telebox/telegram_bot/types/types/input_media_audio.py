from dataclasses import dataclass
from typing import Union, Optional

from telebox.telegram_bot.types.type import Type
from telebox.telegram_bot.consts import input_media_types
from telebox.telegram_bot.types.types.input_file import InputFile
from telebox.telegram_bot.types.types.message_entity import MessageEntity


@dataclass(unsafe_hash=True)
class InputMediaAudio(Type):
    media: str
    thumb: Union[InputFile, str, None] = None
    caption: Optional[str] = None
    parse_mode: Optional[str] = None
    caption_entities: Optional[list[MessageEntity]] = None
    duration: Optional[int] = None
    performer: Optional[str] = None
    title: Optional[str] = None
    type: str = input_media_types.AUDIO
