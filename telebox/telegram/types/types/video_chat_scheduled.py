from dataclasses import dataclass
from datetime import datetime

from telebox.telegram.types.base import Type


@dataclass(unsafe_hash=True)
class VideoChatScheduled(Type):
    start_date: datetime
