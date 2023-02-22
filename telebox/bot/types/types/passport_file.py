from dataclasses import dataclass
from datetime import datetime

from telebox.bot.types.type import Type


@dataclass
class PassportFile(Type):
    file_id: str
    file_unique_id: str
    file_size: int
    file_date: datetime
