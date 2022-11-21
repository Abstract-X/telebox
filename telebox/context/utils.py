from typing import Any, Callable, Optional

from telebox.dispatcher.typing import Event
from telebox.context.vars import event_context
from telebox.context.errors import InvalidEventError
from telebox.dispatcher.utils import events as event_utils


def get_event_chat_id(*, optional: bool = False) -> int:
    return _get_event_value(
        event_utils.get_event_chat_id,
        "chat identifier",
        optional=optional
    )


def get_event_user_id(*, optional: bool = False) -> int:
    return _get_event_value(
        event_utils.get_event_user_id,
        "user identifier",
        optional=optional
    )


def get_event_message_thread_id(*, optional: bool = False) -> Optional[int]:
    return _get_event_value(
        event_utils.get_event_message_thread_id,
        "message thread identifier",
        optional=optional
    )


def get_event_sender_chat_id(*, optional: bool = False) -> int:
    return _get_event_value(
        event_utils.get_event_sender_chat_id,
        "sender chat identifier",
        optional=optional
    )


def get_event_message_id(*, optional: bool = False) -> int:
    return _get_event_value(
        event_utils.get_event_message_id,
        "message identifier",
        optional=optional
    )


def get_event_callback_query_id(*, optional: bool = False) -> str:
    return _get_event_value(
        event_utils.get_event_callback_query_id,
        "callback query identifier",
        optional=optional
    )


def get_event_inline_query_id(*, optional: bool = False) -> str:
    return _get_event_value(
        event_utils.get_event_inline_query_id,
        "inline query identifier",
        optional=optional
    )


def get_event_shipping_query_id(*, optional: bool = False) -> str:
    return _get_event_value(
        event_utils.get_event_shipping_query_id,
        "shipping query identifier",
        optional=optional
    )


def get_event_pre_checkout_query_id(*, optional: bool = False) -> str:
    return _get_event_value(
        event_utils.get_event_pre_checkout_query_id,
        "pre checkout query identifier",
        optional=optional
    )


def _get_event_value(getter: Callable[[Event], Any], name: str, *, optional: bool = False) -> Any:
    event = event_context.get()
    value = getter(event)

    if (not optional) and (value is None):
        raise InvalidEventError(f"No {name} in event" + " {event!r}!", event=event)

    return value
