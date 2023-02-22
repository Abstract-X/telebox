from dataclasses import dataclass

from telebox.bot.types.type import Type


@dataclass
class MessageId(Type):
    message_id: int
