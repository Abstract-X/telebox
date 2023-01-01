from dataclasses import dataclass
from typing import Literal, Optional

from telebox.bot.types.type import Type


@dataclass(eq=False)
class ReplyKeyboardRemove(Type):
    remove_keyboard: Literal[True] = True
    selective: Optional[bool] = None
