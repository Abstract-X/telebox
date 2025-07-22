from attrs import define

from telebox.bot.types.type import Type
from telebox.bot.types.types.photo_size import PhotoSize


@define(repr=False)
class UserProfilePhotos(Type):
    total_count: int
    photos: list[list[PhotoSize]]
