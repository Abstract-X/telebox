from __future__ import annotations
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from telebox.dispatcher.typing import Event
from telebox.dispatcher.utils.media_group import MediaGroup
from telebox.bot.types.types.message import Message
from telebox.bot.types.types.inline_query import InlineQuery
from telebox.bot.types.types.chosen_inline_result import ChosenInlineResult
from telebox.bot.types.types.callback_query import CallbackQuery
from telebox.bot.types.types.shipping_query import ShippingQuery
from telebox.bot.types.types.pre_checkout_query import PreCheckoutQuery
from telebox.bot.types.types.poll import Poll
from telebox.bot.types.types.poll_answer import PollAnswer
from telebox.bot.types.types.chat_member_updated import ChatMemberUpdated
from telebox.bot.types.types.chat_join_request import ChatJoinRequest


TYPES_WITH_CHAT_ID = frozenset({
    Message,
    MediaGroup,
    CallbackQuery,
    ChatMemberUpdated,
    ChatJoinRequest
})
TYPES_WITH_USER_ID = frozenset({
    Message,
    MediaGroup,
    InlineQuery,
    ChosenInlineResult,
    CallbackQuery,
    ShippingQuery,
    PreCheckoutQuery,
    Poll,
    PollAnswer,
    ChatMemberUpdated,
    ChatJoinRequest
})
TYPES_WITH_MESSAGE_THREAD_ID = frozenset({
    Message,
    MediaGroup
})
TYPES_WITH_SENDER_CHAT_ID = frozenset({
    Message,
    MediaGroup
})
TYPES_WITH_MESSAGE_ID = frozenset({
    Message,
    CallbackQuery
})
TYPES_WITH_CALLBACK_QUERY_ID = frozenset({
    CallbackQuery
})
TYPES_WITH_INLINE_QUERY_ID = frozenset({
    InlineQuery
})
TYPES_WITH_SHIPPING_QUERY_ID = frozenset({
    ShippingQuery
})
TYPES_PRE_CHECKOUT_QUERY_ID = frozenset({
    PreCheckoutQuery
})


def get_event_chat_id(event: Event) -> Optional[int]:
    return event.chat_id if type(event) in TYPES_WITH_CHAT_ID else None


def get_event_user_id(event: Event) -> Optional[int]:
    return event.user_id if type(event) in TYPES_WITH_USER_ID else None


def get_event_message_thread_id(event: Event) -> Optional[int]:
    return event.message_thread_id if type(event) in TYPES_WITH_MESSAGE_THREAD_ID else None


def get_event_sender_chat_id(event: Event) -> Optional[int]:
    return event.sender_chat_id if type(event) in TYPES_WITH_SENDER_CHAT_ID else None


def get_event_message_id(event: Event) -> Optional[int]:
    return event.message_id if type(event) in TYPES_WITH_MESSAGE_ID else None


def get_event_callback_query_id(event: Event) -> Optional[str]:
    return event.id if type(event) in TYPES_WITH_CALLBACK_QUERY_ID else None


def get_event_inline_query_id(event: Event) -> Optional[str]:
    return event.id if type(event) in TYPES_WITH_INLINE_QUERY_ID else None


def get_event_shipping_query_id(event: Event) -> Optional[str]:
    return event.id if type(event) in TYPES_WITH_SHIPPING_QUERY_ID else None


def get_event_pre_checkout_query_id(event: Event) -> Optional[str]:
    return event.id if type(event) in TYPES_PRE_CHECKOUT_QUERY_ID else None
