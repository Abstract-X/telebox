from dataclasses import dataclass

from telebox.telegram_bot.types.base import Type


@dataclass(unsafe_hash=True)
class BotCommand(Type):
    command: str
    description: str
