from dataclasses import dataclass
from datetime import datetime

from telebox.bot.types.type import Type


@dataclass
class VideoChatScheduled(Type):
    start_date: datetime
