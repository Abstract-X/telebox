from datetime import datetime
from typing import Optional

from attrs import define

from telebox.bot.type import Type
from telebox.bot.types.poll_option import PollOption
from telebox.bot.types.message_entity import MessageEntity


@define(repr=False)
class Poll(Type):
    id: str
    question: str
    options: list[PollOption]
    total_voter_count: int
    is_closed: bool
    is_anonymous: bool
    type: str
    allows_multiple_answers: bool
    question_entities: Optional[list[MessageEntity]] = None
    correct_option_id: Optional[int] = None
    explanation: Optional[str] = None
    explanation_entities: Optional[list[MessageEntity]] = None
    open_period: Optional[int] = None
    close_date: Optional[datetime] = None
