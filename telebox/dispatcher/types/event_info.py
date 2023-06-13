from dataclasses import dataclass
from typing import Optional

from telebox.dispatcher.typing import Event
from telebox.dispatcher.enums.event_type import EventType


@dataclass
class EventInfo:
    event: Event
    event_type: EventType
    chat_id: Optional[int] = None
    user_id: Optional[int] = None
    from_chat_queue: bool = False
