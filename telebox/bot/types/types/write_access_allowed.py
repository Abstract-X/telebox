from dataclasses import dataclass
from typing import Optional

from telebox.bot.types.type import Type


@dataclass
class WriteAccessAllowed(Type):
    web_app_name: Optional[str] = None
