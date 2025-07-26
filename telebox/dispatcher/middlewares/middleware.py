from telebox.dispatcher.handlers.event import AbstractEventHandler
from telebox.dispatcher.typing import Event
from telebox.dispatcher.enums.event_type import EventType


class Middleware:

    def pre_process_event(
        self,
        event: Event,
        event_type: EventType
    ):
        pass

    def process_event(
        self,
        event: Event,
        event_type: EventType,
        handler: AbstractEventHandler
    ):
        pass

    def post_process_event(
        self,
        event: Event,
        event_type: EventType,
        handler: AbstractEventHandler
    ):
        pass

    def pre_process_error(
        self,
        error: Exception,
        event: Event,
        event_type: EventType
    ):
        pass

    def process_error(
        self,
        error: Exception,
        event: Event,
        event_type: EventType
    ):
        pass

    def post_process_error(
        self,
        error: Exception,
        event: Event,
        event_type: EventType
    ):
        pass
