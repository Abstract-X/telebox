from dataclasses import dataclass
from typing import Optional

from telebox.telegram_bot.types.type import Type
from telebox.telegram_bot.types.types.photo_size import PhotoSize
from telebox.telegram_bot.types.types.message_entity import MessageEntity
from telebox.telegram_bot.types.types.animation import Animation


@dataclass(unsafe_hash=True)
class Game(Type):
    title: str
    description: str
    photo: list[PhotoSize]
    text: Optional[str] = None
    text_entities: Optional[list[MessageEntity]] = None
    animation: Optional[Animation] = None
