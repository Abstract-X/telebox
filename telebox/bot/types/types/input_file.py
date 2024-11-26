from dataclasses import dataclass, field
from typing import Optional, BinaryIO, Union
from pathlib import Path
import os.path

from telebox.bot.types.type import Type
from telebox.bot.enums.input_file_type import InputFileType


@dataclass(repr=False)
class InputFile(Type):
    file: Union[str, Path, BinaryIO, None] = field(repr=False)
    name: Optional[str] = None

    def __post_init__(self):
        if self.type is InputFileType.PATH:
            self.file = Path(self.file).resolve()

            if not self.file.exists():
                raise ValueError(f"File doesn't exist {self.file!r}!")

            if not self.file.is_file():
                raise ValueError(f"File is not file {self.file!r}!")

        if not self.name:
            if self.type is InputFileType.FILE:
                if hasattr(self.file, "name"):
                    self.name = os.path.basename(self.file.name)
            elif self.type is InputFileType.PATH:
                self.name = self.file.name

        if not self.name:
            self.name = "untitled"

    @property
    def type(self) -> InputFileType:
        if isinstance(self.file, (Path, str)):
            return InputFileType.PATH
        else:
            return InputFileType.FILE
