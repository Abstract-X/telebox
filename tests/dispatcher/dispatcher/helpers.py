from typing import Literal

from telebox import EventType, MediaGroup, AbstractEventHandler, AbstractEventFilter
from telebox.telegram_bot.types import Message, InlineQuery, CallbackQuery


class MessageHandler(AbstractEventHandler):

    def process_event(self, event: Message) -> None:
        pass


class EditedMessageHandler(AbstractEventHandler):

    def process_event(self, event: Message) -> None:
        pass


class ChannelPostHandler(AbstractEventHandler):

    def process_event(self, event: Message) -> None:
        pass


class EditedChannelPostHandler(AbstractEventHandler):

    def process_event(self, event: Message) -> None:
        pass


class MediaGroupHandler(AbstractEventHandler):

    def process_event(self, event: MediaGroup) -> None:
        pass


class InlineQueryHandler(AbstractEventHandler):

    def process_event(self, event: InlineQuery) -> None:
        pass


class MessageFilter(AbstractEventFilter):

    def get_event_types(self) -> set[EventType]:
        return {EventType.MESSAGE}

    def get_value(self, event: Message) -> Literal[True]:
        return True

    def check_value(self, value: bool) -> bool:
        return value


class EditedMessageFilter(AbstractEventFilter):

    def get_event_types(self) -> set[EventType]:
        return {EventType.EDITED_MESSAGE}

    def get_value(self, event: Message) -> Literal[True]:
        return True

    def check_value(self, value: bool) -> bool:
        return value


class ChannelPostFilter(AbstractEventFilter):

    def get_event_types(self) -> set[EventType]:
        return {EventType.CHANNEL_POST}

    def get_value(self, event: Message) -> Literal[True]:
        return True

    def check_value(self, value: bool) -> bool:
        return value


class EditedChannelPostFilter(AbstractEventFilter):

    def get_event_types(self) -> set[EventType]:
        return {EventType.EDITED_CHANNEL_POST}

    def get_value(self, event: Message) -> Literal[True]:
        return True

    def check_value(self, value: bool) -> bool:
        return value


class MediaGroupFilter(AbstractEventFilter):

    def get_event_types(self) -> set[EventType]:
        return {EventType.MEDIA_GROUP}

    def get_value(self, event: MediaGroup) -> Literal[True]:
        return True

    def check_value(self, value: bool) -> bool:
        return value


class InlineQueryFilter(AbstractEventFilter):

    def get_event_types(self) -> set[EventType]:
        return {EventType.INLINE_QUERY}

    def get_value(self, event: InlineQuery) -> Literal[True]:
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
