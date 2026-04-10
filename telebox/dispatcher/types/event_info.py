from dataclasses import dataclass
from typing import Optional

from telebox.dispatcher.context import EventContext
from telebox.dispatcher.type_hints import Event
from telebox.dispatcher.enums.event_type import EventType
from telebox.dispatcher.enums.processing_status import ProcessingStatus


@dataclass
class EventInfo:
    event: Event
    event_type: EventType
    ctx: Optional[EventContext] = None
    chat_id: Optional[int] = None
    user_id: Optional[int] = None
    from_chat_queue: bool = False
    use_chat_queue: bool = False
    is_pre_processed: bool = False
    processing_status: ProcessingStatus = ProcessingStatus.PROCESSING

    def __post_init__(self):
        if hasattr(self.event, "chat_id"):
            self.chat_id = self.event.chat_id

        if hasattr(self.event, "user_id"):
            self.user_id = self.event.user_id
