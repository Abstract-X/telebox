from telebox.dispatcher.middlewares.middleware import Middleware
from telebox.dispatcher.typing import Event
from telebox.dispatcher.enums.event_type import EventType
from telebox.utils.callback_data_builders.builder import AbstractCallbackDataBuilder


class CallbackDataMiddleware(Middleware):

    def __init__(self, builder: AbstractCallbackDataBuilder):
        self._builder = builder

    def process_event(self, event: Event, event_type: EventType) -> None:
        if event_type is EventType.CALLBACK_QUERY:
            _, event.data = self._builder.parse(event.data)
