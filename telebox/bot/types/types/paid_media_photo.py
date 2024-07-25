from dataclasses import dataclass

from telebox.bot.types.type import Type
from telebox.bot.consts import paid_media_types
from telebox.bot.types.types.photo_size import PhotoSize


@dataclass(repr=False)
class PaidMediaPhoto(Type):
    photo: list[PhotoSize]
    type: str = paid_media_types.PHOTO
