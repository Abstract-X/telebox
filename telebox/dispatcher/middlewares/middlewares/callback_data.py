from telebox.dispatcher.middlewares.middleware import Middleware
from telebox.dispatcher.dispatcher import Event
from telebox.dispatcher.enums.event_type import EventType
from telebox.telegram_bot.types.types.callback_query import CallbackQuery
from telebox.utils.callback_data_builders.builder import AbstractCallbackDataBuilder


class CallbackDataMiddleware(Middleware):

    def __init__(self, builder: AbstractCallbackDataBuilder):
        self._builder = builder

    def process_event(self, event: Event, event_type: EventType) -> None:
        if isinstance(event, CallbackQuery):
            _, event.data = self._builder.parse(event.data)
