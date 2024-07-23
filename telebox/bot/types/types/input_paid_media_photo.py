from dataclasses import dataclass
from typing import Union

from telebox.bot.types.type import Type
from telebox.bot.consts import input_paid_media_types
from telebox.bot.types.types.input_file import InputFile


@dataclass(repr=False)
class InputPaidMediaPhoto(Type):
    media: Union[InputFile, str]
    type: str = input_paid_media_types.PHOTO
