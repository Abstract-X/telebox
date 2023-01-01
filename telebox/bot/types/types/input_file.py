from dataclasses import dataclass, field
from typing import Optional

from telebox.bot.types.type import Type


@dataclass(eq=False)
class InputFile(Type):
    content: bytes = field(repr=False)
    name: Optional[str] = None
