from typing import Optional

from attrs import define

from telebox.bot.type import Type
from telebox.bot.types.photo_size import PhotoSize
from telebox.bot.types.message_entity import MessageEntity
from telebox.bot.types.animation import Animation


@define(repr=False)
class Game(Type):
    title: str
    description: str
    photo: list[PhotoSize]
    text: Optional[str] = None
    text_entities: Optional[list[MessageEntity]] = None
    animation: Optional[Animation] = None
