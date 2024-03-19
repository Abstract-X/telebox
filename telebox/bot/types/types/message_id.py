from dataclasses import dataclass

from telebox.bot.types.type import Type


@dataclass(repr=False)
class MessageId(Type):
    message_id: int
