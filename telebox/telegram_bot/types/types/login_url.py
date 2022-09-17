from dataclasses import dataclass
from typing import Optional

from telebox.telegram_bot.types.base import Type


@dataclass(unsafe_hash=True)
class LoginUrl(Type):
    url: str
    forward_text: Optional[str] = None
    bot_username: Optional[str] = None
    request_write_access: Optional[bool] = None
