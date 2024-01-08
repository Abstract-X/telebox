from dataclasses import dataclass
from typing import Optional

from telebox.bot.types.type import Type


@dataclass
class LinkPreviewOptions(Type):
    is_disabled: Optional[bool] = None
    url: Optional[str] = None
    prefer_small_media: Optional[bool] = None
    prefer_large_media: Optional[bool] = None
    show_above_text: Optional[bool] = None
