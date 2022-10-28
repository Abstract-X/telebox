from typing import Literal

from telebox import EventType, AbstractEventHandler, AbstractEventFilter
from telebox.telegram_bot.types import Message, CallbackQuery


class MessageHandler(AbstractEventHandler):

    def process_event(self, event: Message) -> None:
        pass


class MessageFilter(AbstractEventFilter):

    def get_event_types(self) -> set[EventType]:
        return {EventType.MESSAGE}

    def get_value(self, event: Message) -> Literal[True]:
        return True

    def check_value(self, value: bool) -> bool:
        return value


class CallbackQueryFilter(AbstractEventFilter):

    def get_event_types(self) -> set[EventType]:
        return {EventType.CALLBACK_QUERY}

    def get_value(self, event: CallbackQuery) -> Literal[True]:
        return True

    def check_value(self, value: bool) -> bool:
        return value
