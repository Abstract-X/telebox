from dataclasses import dataclass
from typing import Optional, BinaryIO, Union
from pathlib import Path
import os.path

from telebox.bot.types.type import Type


@dataclass(repr=False)
class InputFile(Type):

    def __init__(
        self,
        *,
        file: Optional[BinaryIO] = None,
        file_path: Union[str, Path, None] = None,
        name: Optional[str] = None
    ):
        if sum(i is not None for i in (file, file_path)) != 1:
            raise ValueError("One value is allowed: «file» or «file_path»!")

        if file_path is not None:
            file_path = Path(file_path).resolve()

            if not file_path.exists():
                raise ValueError(f"«file_path» doesn't exist {file_path!r}!")

            if not file_path.is_file():
                raise ValueError(f"«file_path» is not file {file_path!r}!")

        if not name:
            if file is not None:
                if hasattr(file, "name"):
                    name = os.path.basename(file.name)
            elif file_path is not None:
                name = file_path.name

        self.file = file
        self.file_path = file_path
        self.name = name or "untitled"
