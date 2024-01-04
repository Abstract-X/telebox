from typing import Union

from telebox.bot.types.types.message import Message
from telebox.bot.types.types.inaccessible_message import InaccessibleMessage


MaybeInaccessibleMessage = Union[Message, InaccessibleMessage]
