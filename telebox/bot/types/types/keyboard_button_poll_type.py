from dataclasses import dataclass
from typing import Optional

from telebox.bot.types.type import Type


@dataclass(eq=False)
class KeyboardButtonPollType(Type):
    type: Optional[str] = None
