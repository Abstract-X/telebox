from typing import Any, Type

from telebox.dispatcher.typing import Event
from telebox.dispatcher.media_group import MediaGroup
from telebox.context.vars import event_context
from telebox.context.errors import InvalidEventError
from telebox.telegram_bot.types.types.message import Message
from telebox.telegram_bot.types.types.inline_query import InlineQuery
from telebox.telegram_bot.types.types.chosen_inline_result import ChosenInlineResult
from telebox.telegram_bot.types.types.callback_query import CallbackQuery
from telebox.telegram_bot.types.types.shipping_query import ShippingQuery
from telebox.telegram_bot.types.types.pre_checkout_query import PreCheckoutQuery
from telebox.telegram_bot.types.types.poll_answer import PollAnswer
from telebox.telegram_bot.types.types.chat_member_updated import ChatMemberUpdated
from telebox.telegram_bot.types.types.chat_join_request import ChatJoinRequest


def get_event_chat_id() -> int:
    return _get_event_value(
        attribute="chat_id",
        name="chat identifier",
        types=(Message, CallbackQuery, MediaGroup, ChatMemberUpdated, ChatJoinRequest)
    )


def get_event_user_id() -> int:
    return _get_event_value(
        attribute="user_id",
        name="user identifier",
        types=(
            Message,
            InlineQuery,
            ChosenInlineResult,
            CallbackQuery,
            MediaGroup,
            ShippingQuery,
            PreCheckoutQuery,
            PollAnswer,
            ChatMemberUpdated,
            ChatJoinRequest
        )
    )


def get_event_sender_chat_id() -> int:
    return _get_event_value(
        attribute="sender_chat_id",
        name="sender chat identifier",
        types=(Message, MediaGroup)
    )


def get_event_message_id() -> int:
    return _get_event_value(
        attribute="message_id",
        name="message identifier",
        types=(Message, CallbackQuery)
    )


def get_event_callback_query_id() -> str:
    return _get_event_value(
        attribute="id",
        name="callback query identifier",
        types=(CallbackQuery,)
    )


def get_event_inline_query_id() -> str:
    return _get_event_value(
        attribute="id",
        name="inline query identifier",
        types=(InlineQuery,)
    )


def get_event_shipping_query_id() -> str:
    return _get_event_value(
        attribute="id",
        name="shipping query identifier",
        types=(ShippingQuery,)
    )


def get_event_pre_checkout_query_id() -> str:
    return _get_event_value(
        attribute="id",
        name="pre checkout query identifier",
        types=(PreCheckoutQuery,)
    )


def _get_event_value(attribute: str, name: str, types: tuple[Type[Event], ...]) -> Any:
    event = event_context.get()

    if (not isinstance(event, types)) or (getattr(event, attribute) is None):
        raise InvalidEventError(
            f"No {name} in event" + " {event!r}!",
            event=event
        ) from None

    return getattr(event, attribute)
