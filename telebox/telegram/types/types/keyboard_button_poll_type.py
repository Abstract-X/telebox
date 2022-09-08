from dataclasses import dataclass
from typing import Optional

from telebox.telegram.types.base import Type


@dataclass(unsafe_hash=True)
class KeyboardButtonPollType(Type):
    type: Optional[str] = None
