from dataclasses import dataclass
from typing import Optional

from telebox.bot.types.type import Type
from telebox.bot.utils.users import get_full_name


@dataclass(eq=False)
class InputContactMessageContent(Type):
    phone_number: str
    first_name: str
    last_name: Optional[str] = None
    vcard: Optional[str] = None

    @property
    def full_name(self) -> str:
        return get_full_name(self.first_name, self.last_name)
