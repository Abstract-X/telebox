from dataclasses import dataclass
from typing import Optional

from telebox.bot.types.type import Type
from telebox.bot.consts import paid_media_types


@dataclass(repr=False)
class PaidMediaPreview(Type):
    width: Optional[int] = None
    height: Optional[int] = None
    duration: Optional[int] = None
    type: str = paid_media_types.PREVIEW
