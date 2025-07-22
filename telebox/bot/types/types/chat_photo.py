from attrs import define

from telebox.bot.types.type import Type


@define(repr=False)
class ChatPhoto(Type):
    small_file_id: str
    small_file_unique_id: str
    big_file_id: str
    big_file_unique_id: str
