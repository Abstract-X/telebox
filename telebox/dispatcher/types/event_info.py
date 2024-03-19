from dataclasses import dataclass
from typing import Optional

from telebox.dispatcher.typing import Event
from telebox.dispatcher.enums.event_type import EventType
from telebox.dispatcher.enums.processing_status import ProcessingStatus


@dataclass
class EventInfo:
    event: Event
    event_type: EventType
    chat_id: Optional[int] = None
    user_id: Optional[int] = None
    from_chat_queue: bool = False
    with_chat_queue: bool = False
    busy_threads_processed: bool = False
    middleware_pre_processed: bool = False
    processing_status: ProcessingStatus = ProcessingStatus.PROCESSING
