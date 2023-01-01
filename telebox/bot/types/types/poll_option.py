from dataclasses import dataclass

from telebox.bot.types.type import Type


@dataclass(eq=False)
class PollOption(Type):
    text: str
    voter_count: int
