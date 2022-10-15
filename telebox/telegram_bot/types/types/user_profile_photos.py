from dataclasses import dataclass

from telebox.telegram_bot.types.type import Type
from telebox.telegram_bot.types.types.photo_size import PhotoSize


@dataclass(unsafe_hash=True)
class UserProfilePhotos(Type):
    total_count: int
    photos: list[list[PhotoSize]]
