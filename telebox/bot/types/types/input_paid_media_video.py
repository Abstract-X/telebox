from dataclasses import dataclass
from typing import Union, Optional

from telebox.bot.types.type import Type
from telebox.bot.consts import input_paid_media_types
from telebox.bot.types.types.input_file import InputFile


@dataclass(repr=False)
class InputPaidMediaVideo(Type):
    media: Union[InputFile, str]
    thumbnail: Union[InputFile, str, None] = None
    width: Optional[int] = None
    height: Optional[int] = None
    duration: Optional[int] = None
    supports_streaming: Optional[bool] = None
    type: str = input_paid_media_types.VIDEO
