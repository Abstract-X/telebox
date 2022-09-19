from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from telebox.telegram_bot.types.base import Type
from telebox.telegram_bot.types.types.poll_option import PollOption
from telebox.telegram_bot.types.types.message_entity import MessageEntity


@dataclass(unsafe_hash=True)
class Poll(Type):
    id: str
    question: str
    options: list[PollOption]
    total_voter_count: int
    is_closed: bool
    is_anonymous: bool
    type: str
    allows_multiple_answers: bool
    correct_option_id: Optional[int] = None
    explanation: Optional[str] = None
    explanation_entities: Optional[list[MessageEntity]] = None
    open_period: Optional[int] = None
    close_date: Optional[datetime] = None
