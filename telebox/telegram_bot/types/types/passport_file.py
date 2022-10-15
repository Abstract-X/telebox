from dataclasses import dataclass
from datetime import datetime

from telebox.telegram_bot.types.type import Type


@dataclass(unsafe_hash=True)
class PassportFile(Type):
    file_id: str
    file_unique_id: str
    file_size: int
    file_date: datetime
