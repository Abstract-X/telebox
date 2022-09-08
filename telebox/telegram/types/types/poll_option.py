from dataclasses import dataclass

from telebox.telegram.types.base import Type


@dataclass(unsafe_hash=True)
class PollOption(Type):
    text: str
    voter_count: int
