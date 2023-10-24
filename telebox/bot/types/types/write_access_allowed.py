from dataclasses import dataclass
from typing import Optional

from telebox.bot.types.type import Type


@dataclass
class WriteAccessAllowed(Type):
    from_request: Optional[bool] = None
    web_app_name: Optional[str] = None
    from_attachment_menu: Optional[bool] = None
