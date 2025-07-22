from typing import Union, Optional

from attrs import define

from telebox.bot.types.type import Type
from telebox.bot.types.types.input_file import InputFile
from telebox.bot.types.types.mask_position import MaskPosition


@define(repr=False)
class InputSticker(Type):
    sticker: Union[InputFile, str]
    format: str
    emoji_list: list[str]
    mask_position: Optional[MaskPosition] = None
    keywords: Optional[list[str]] = None
