from typing import BinaryIO, Union
import secrets
from pathlib import Path
import os.path

from attrs import define, field

from telebox.bot.type import Type
from telebox.bot.enums.input_file_type import InputFileType
from telebox.utils.unset import Unset, UNSET


@define(repr=False)
class InputFile(Type):
    file: Union[str, Path, BinaryIO] = field(repr=False)
    name: Union[str, None, Unset] = field(default=UNSET, kw_only=True)

    def __attrs_post_init__(self):
        if isinstance(self.file, str):
            self.file = Path(self.file)

        if self.type is InputFileType.PATH:
            self.file = self.file.resolve()

        if not self.name:
            if self.type is InputFileType.FILE:
                if hasattr(self.file, "name"):
                    self.name = os.path.basename(self.file.name)
            elif self.type is InputFileType.PATH:
                self.name = self.file.name

        if not self.name:
            self.name = secrets.token_urlsafe(12)

    @property
    def type(self) -> InputFileType:
        if isinstance(self.file, Path):
            return InputFileType.PATH
        else:
            return InputFileType.FILE
