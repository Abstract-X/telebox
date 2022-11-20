from dataclasses import dataclass
from typing import Optional

from telebox.bot.types.type import Type


@dataclass(unsafe_hash=True)
class KeyboardButtonPollType(Type):
    type: Optional[str] = None
