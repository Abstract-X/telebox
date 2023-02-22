from dataclasses import dataclass
from typing import Optional

from telebox.bot.types.type import Type


@dataclass
class KeyboardButtonPollType(Type):
    type: Optional[str] = None
