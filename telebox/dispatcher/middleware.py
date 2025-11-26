from telebox.dispatcher.type_hints import Event, Handler
from telebox.dispatcher.enums.event_type import EventType
from telebox.utils.data import Data


class Middleware:
    def pre_process_event(
        self,
        deps,
        event: Event,
        event_type: EventType,
        data: Data
    ) -> None:
        pass

    def process_event(
        self,
        deps,
        event: Event,
        event_type: EventType,
        data: Data,
        handler: Handler
    ) -> None:
        pass

    def post_process_event(
        self,
        deps,
        event: Event,
        event_type: EventType,
        data: Data,
        handler: Handler
    ):
        pass

    def pre_process_error(
        self,
        deps,
        error: Exception,
        event: Event,
        event_type: EventType
    ):
        pass

    def process_error(
        self,
        deps,
        error: Exception,
        event: Event,
        event_type: EventType
    ):
        pass

    def post_process_error(
        self,
        deps,
        error: Exception,
        event: Event,
        event_type: EventType
    ):
        pass
