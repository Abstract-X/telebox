from typing import Optional

from telebox.dispatcher.handlers.event import AbstractEventHandler
from telebox.dispatcher.typing import Event
from telebox.dispatcher.enums.event_type import EventType
from telebox.dispatcher.types.aborting import Aborting


class Middleware:

    def pre_process_event(
        self,
        event: Event,
        event_type: EventType
    ) -> Optional[Aborting]:
        pass

    def process_event(
        self,
        event: Event,
        event_type: EventType,
        handler: AbstractEventHandler
    ) -> Optional[Aborting]:
        pass

    def post_process_event(
        self,
        event: Event,
        event_type: EventType,
        handler: AbstractEventHandler
    ) -> Optional[Aborting]:
        pass

    def pre_process_error(
        self,
        error: Exception,
        event: Event,
        event_type: EventType
    ) -> Optional[Aborting]:
        pass

    def process_error(
        self,
        error: Exception,
        event: Event,
        event_type: EventType
    ) -> Optional[Aborting]:
        pass

    def post_process_error(
        self,
        error: Exception,
        event: Event,
        event_type: EventType
    ) -> Optional[Aborting]:
        pass
