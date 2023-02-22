from dataclasses import dataclass
from typing import Optional

from telebox.bot.types.type import Type


@dataclass
class LoginUrl(Type):
    url: str
    forward_text: Optional[str] = None
    bot_username: Optional[str] = None
    request_write_access: Optional[bool] = None
