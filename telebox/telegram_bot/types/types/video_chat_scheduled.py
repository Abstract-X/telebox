from dataclasses import dataclass
from datetime import datetime

from telebox.telegram_bot.types.type import Type


@dataclass(unsafe_hash=True)
class VideoChatScheduled(Type):
    start_date: datetime
