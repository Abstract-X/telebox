from dataclasses import dataclass

from telebox.bot.types.type import Type
from telebox.bot.types.types.photo_size import PhotoSize


@dataclass
class UserProfilePhotos(Type):
    total_count: int
    photos: list[list[PhotoSize]]
