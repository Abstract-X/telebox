from dataclasses import dataclass

from telebox.bot.types.type import Type


@dataclass(repr=False)
class ChatShared(Type):
    request_id: int
    chat_id: int
