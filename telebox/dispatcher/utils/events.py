from __future__ import annotations
from typing import Any, Optional, Iterable, TYPE_CHECKING

if TYPE_CHECKING:
    from telebox.dispatcher.typing import Event
from telebox.dispatcher.errors import InvalidEventError
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


def get_event_chat_id(event: Event, *, strictly: bool = False) -> Optional[int]:
    return _get_event_attribute(
        attribute="chat_id",
        name="chat identifier",
        event=event,
        types=frozenset((
            Message,
            MediaGroup,
            CallbackQuery,
            ChatMemberUpdated,
            ChatJoinRequest
        )),
        strictly=strictly
    )


def get_event_user_id(event: Event, *, strictly: bool = False) -> Optional[int]:
    return _get_event_attribute(
        attribute="user_id",
        name="user identifier",
        event=event,
        types=frozenset((
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
        )),
        strictly=strictly
    )


def get_event_message_topic_id(event: Event, *, strictly: bool = False) -> Optional[int]:
    return _get_event_attribute(
        attribute="message_topic_id",
        name="message topic identifier",
        event=event,
        types=frozenset((Message, MediaGroup)),
        strictly=strictly
    )


def get_event_sender_chat_id(event: Event, *, strictly: bool = False) -> Optional[int]:
    return _get_event_attribute(
        attribute="sender_chat_id",
        name="sender chat identifier",
        event=event,
        types=frozenset((Message, MediaGroup)),
        strictly=strictly
    )


def get_event_message_id(event: Event, *, strictly: bool = False) -> Optional[int]:
    return _get_event_attribute(
        attribute="message_id",
        name="message identifier",
        event=event,
        types=frozenset((Message, MediaGroup, CallbackQuery)),
        strictly=strictly
    )


def get_event_callback_query_id(event: Event, *, strictly: bool = False) -> Optional[str]:
    return _get_event_attribute(
        attribute="id",
        name="callback query identifier",
        event=event,
        types=(CallbackQuery,),
        strictly=strictly
    )


def get_event_inline_query_id(event: Event, *, strictly: bool = False) -> Optional[str]:
    return _get_event_attribute(
        attribute="id",
        name="inline query identifier",
        event=event,
        types=(InlineQuery,),
        strictly=strictly
    )


def get_event_shipping_query_id(event: Event, *, strictly: bool = False) -> Optional[str]:
    return _get_event_attribute(
        attribute="id",
        name="shipping query identifier",
        event=event,
        types=(ShippingQuery,),
        strictly=strictly
    )


def get_event_pre_checkout_query_id(event: Event, *, strictly: bool = False) -> Optional[str]:
    return _get_event_attribute(
        attribute="id",
        name="pre checkout query identifier",
        event=event,
        types=(PreCheckoutQuery,),
        strictly=strictly
    )


def _get_event_attribute(
    attribute,
    name: str,
    event: Event,
    types: Iterable[type],
    *,
    strictly: bool
) -> Any:
    if type(event) in types:
        return getattr(event, attribute)
    elif strictly:
        raise InvalidEventError(f"No {name} in event" + " {event!r}!", event=event)
