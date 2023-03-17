from dataclasses import dataclass
from typing import Union, Optional

from telebox.bot.types.type import Type
from telebox.bot.types.types.input_file import InputFile
from telebox.bot.types.types.mask_position import MaskPosition


@dataclass
class InputSticker(Type):
    sticker: Union[InputFile, str]
    emoji_list: list[str]
    mask_position: Optional[MaskPosition] = None
    keywords: Optional[list[str]] = None
