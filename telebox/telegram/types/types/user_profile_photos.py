from dataclasses import dataclass

from telebox.telegram.types.base import Type
from telebox.telegram.types.types.photo_size import PhotoSize


@dataclass(unsafe_hash=True)
class UserProfilePhotos(Type):
    total_count: int
    photos: list[list[PhotoSize]]
