from typing import Literal

from telebox import EventType, MediaGroup, AbstractEventHandler, AbstractEventFilter
from telebox.telegram_bot.types import (
    Message,
    InlineQuery,
    ChosenInlineResult,
    CallbackQuery,
    ShippingQuery,
    PreCheckoutQuery,
    Poll
)


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


class ChosenInlineResultHandler(AbstractEventHandler):

    def process_event(self, event: ChosenInlineResult) -> None:
        pass


class CallbackQueryHandler(AbstractEventHandler):

    def process_event(self, event: CallbackQuery) -> None:
        pass


class ShippingQueryHandler(AbstractEventHandler):

    def process_event(self, event: ShippingQuery) -> None:
        pass


class PreCheckoutQueryHandler(AbstractEventHandler):

    def process_event(self, event: PreCheckoutQuery) -> None:
        pass


class PollHandler(AbstractEventHandler):

    def process_event(self, event: Poll) -> None:
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


class ChosenInlineResultFilter(AbstractEventFilter):

    def get_event_types(self) -> set[EventType]:
        return {EventType.CHOSEN_INLINE_RESULT}

    def get_value(self, event: ChosenInlineResult) -> Literal[True]:
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


class ShippingQueryFilter(AbstractEventFilter):

    def get_event_types(self) -> set[EventType]:
        return {EventType.SHIPPING_QUERY}

    def get_value(self, event: ShippingQuery) -> Literal[True]:
        return True

    def check_value(self, value: bool) -> bool:
        return value


class PreCheckoutQueryFilter(AbstractEventFilter):

    def get_event_types(self) -> set[EventType]:
        return {EventType.PRE_CHECKOUT_QUERY}

    def get_value(self, event: PreCheckoutQuery) -> Literal[True]:
        return True

    def check_value(self, value: bool) -> bool:
        return value


class PollFilter(AbstractEventFilter):

    def get_event_types(self) -> set[EventType]:
        return {EventType.POLL}

    def get_value(self, event: Poll) -> Literal[True]:
        return True

    def check_value(self, value: bool) -> bool:
        return value
