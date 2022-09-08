from dataclasses import dataclass
from typing import Optional

from telebox.telegram.types.base import Type
from telebox.telegram.types.types.photo_size import PhotoSize
from telebox.telegram.types.types.message_entity import MessageEntity
from telebox.telegram.types.types.animation import Animation


@dataclass(unsafe_hash=True)
class Game(Type):
    title: str
    description: str
    photo: list[PhotoSize]
    text: Optional[str] = None
    text_entities: Optional[list[MessageEntity]] = None
    animation: Optional[Animation] = None
