from dataclasses import dataclass
from typing import Optional

from telebox.bot.types.type import Type


@dataclass(repr=False)
class KeyboardButtonRequestUsers(Type):
    request_id: int
    user_is_bot: Optional[bool] = None
    user_is_premium: Optional[bool] = None
    max_quantity: Optional[int] = None
    request_name: Optional[bool] = None
    request_username: Optional[bool] = None
    request_photo: Optional[bool] = None
