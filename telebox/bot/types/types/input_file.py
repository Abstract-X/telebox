from dataclasses import dataclass, field
from typing import Optional, BinaryIO
import os.path

from telebox.bot.types.type import Type


@dataclass
class InputFile(Type):
    file: BinaryIO = field(repr=False)
    name: Optional[str] = None

    def __post_init__(self):
        if (self.name is None) and hasattr(self.file, "name"):
            self.name = os.path.basename(self.file.name)
