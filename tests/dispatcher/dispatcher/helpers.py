from typing import Literal

from telebox import (
    Event,
    EventType,
    MediaGroup,
    AbstractEventHandler,
    AbstractErrorHandler,
    AbstractEventFilter,
    AbstractErrorFilter
)
from telebox.telegram_bot.types import (
    Message,
    InlineQuery,
    ChosenInlineResult,
    CallbackQuery,
    ShippingQuery,
    PreCheckoutQuery,
    Poll,
    PollAnswer,
    ChatMemberUpdated,
    ChatJoinRequest
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


class PollAnswerHandler(AbstractEventHandler):

    def process_event(self, event: PollAnswer) -> None:
        pass


class MyChatMemberHandler(AbstractEventHandler):

    def process_event(self, event: ChatMemberUpdated) -> None:
        pass


class ChatMemberHandler(AbstractEventHandler):

    def process_event(self, event: ChatMemberUpdated) -> None:
        pass


class ChatJoinRequestHandler(AbstractEventHandler):

    def process_event(self, event: ChatJoinRequest) -> None:
        pass


class ErrorHandler(AbstractErrorHandler):

    def process_error(self, error: Exception, event: Event) -> None:
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


class PollAnswerFilter(AbstractEventFilter):

    def get_event_types(self) -> set[EventType]:
        return {EventType.POLL_ANSWER}

    def get_value(self, event: PollAnswer) -> Literal[True]:
        return True

    def check_value(self, value: bool) -> bool:
        return value


class MyChatMemberFilter(AbstractEventFilter):

    def get_event_types(self) -> set[EventType]:
        return {EventType.MY_CHAT_MEMBER}

    def get_value(self, event: ChatMemberUpdated) -> Literal[True]:
        return True

    def check_value(self, value: bool) -> bool:
        return value


class ChatMemberFilter(AbstractEventFilter):

    def get_event_types(self) -> set[EventType]:
        return {EventType.CHAT_MEMBER}

    def get_value(self, event: ChatMemberUpdated) -> Literal[True]:
        return True

    def check_value(self, value: bool) -> bool:
        return value


class ChatJoinRequestFilter(AbstractEventFilter):

    def get_event_types(self) -> set[EventType]:
        return {EventType.CHAT_JOIN_REQUEST}

    def get_value(self, event: ChatJoinRequest) -> Literal[True]:
        return True

    def check_value(self, value: bool) -> bool:
        return value


class ErrorFilter(AbstractErrorFilter):

    def get_value(self, error: Exception, event: Event) -> Literal[True]:
        return True

    def check_value(self, value: bool) -> bool:
        return value
