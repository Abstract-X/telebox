from dataclasses import dataclass
from typing import Optional

from telebox.bot.types.type import Type


@dataclass
class KeyboardButtonRequestUsers(Type):
    request_id: int
    user_is_bot: Optional[bool] = None
    user_is_premium: Optional[bool] = None
    max_quantity: Optional[int] = None
