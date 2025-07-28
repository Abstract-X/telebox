from attrs import define

from telebox.bot.type import Type
from telebox.bot.consts import paid_media_types
from telebox.bot.types.photo_size import PhotoSize


@define(repr=False)
class PaidMediaPhoto(Type):
    photo: list[PhotoSize]
    type: str = paid_media_types.PHOTO
