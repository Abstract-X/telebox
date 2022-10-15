from dataclasses import dataclass, field
from typing import Optional

from telebox.telegram_bot.types.type import Type


@dataclass(unsafe_hash=True)
class InputFile(Type):
    content: bytes = field(repr=False)
    name: Optional[str] = None
