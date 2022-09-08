from dataclasses import dataclass

from telebox.telegram.types.base import Type


@dataclass(unsafe_hash=True)
class ChatPhoto(Type):
    small_file_id: str
    small_file_unique_id: str
    big_file_id: str
    big_file_unique_id: str
