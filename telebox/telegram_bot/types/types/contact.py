from dataclasses import dataclass
from typing import Optional

from telebox.telegram_bot.types.type import Type
from telebox.telegram_bot.utils import get_full_name


@dataclass(unsafe_hash=True)
class Contact(Type):
    phone_number: str
    first_name: str
    last_name: Optional[str] = None
    user_id: Optional[int] = None
    vcard: Optional[str] = None

    @property
    def full_name(self) -> str:
        return get_full_name(self.first_name, self.last_name)
