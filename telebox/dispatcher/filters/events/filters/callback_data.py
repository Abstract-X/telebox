from telebox.dispatcher.filters.events.filter import AbstractEventFilter
from telebox.dispatcher.enums.event_type import EventType
from telebox.bot.types.types.callback_query import CallbackQuery


class CallbackDataFilter(AbstractEventFilter):

    def __init__(self, *data: str):
        self._data = set(data)

    def get_event_types(self) -> set[EventType]:
        return {EventType.CALLBACK_QUERY}

    def check_event(self, event: CallbackQuery) -> bool:
        return event.data in self._data if self._data else event.data is not None
