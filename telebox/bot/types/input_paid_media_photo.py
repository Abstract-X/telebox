from typing import Union

from attrs import define

from telebox.bot.type import Type
from telebox.bot.consts import input_paid_media_types
from telebox.bot.types.input_file import InputFile


@define(repr=False)
class InputPaidMediaPhoto(Type):
    media: Union[InputFile, str]
    type: str = input_paid_media_types.PHOTO
