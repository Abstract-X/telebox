from typing import Any, Callable

from telebox.dispatcher.typing import Event
from telebox.context.vars import event_context
from telebox.context.errors import InvalidEventError
from telebox.dispatcher.utils import events as event_utils


def get_event_chat_id() -> int:
    return _get_event_value(
        event_utils.get_event_chat_id,
        "chat identifier"
    )


def get_event_user_id() -> int:
    return _get_event_value(
        event_utils.get_event_user_id,
        "user identifier"
    )


def get_event_sender_chat_id() -> int:
    return _get_event_value(
        event_utils.get_event_sender_chat_id,
        "sender chat identifier"
    )


def get_event_message_id() -> int:
    return _get_event_value(
        event_utils.get_event_message_id,
        "message identifier"
    )


def get_event_callback_query_id() -> str:
    return _get_event_value(
        event_utils.get_event_callback_query_id,
        "callback query identifier"
    )


def get_event_inline_query_id() -> str:
    return _get_event_value(
        event_utils.get_event_inline_query_id,
        "inline query identifier"
    )


def get_event_shipping_query_id() -> str:
    return _get_event_value(
        event_utils.get_event_shipping_query_id,
        "shipping query identifier"
    )


def get_event_pre_checkout_query_id() -> str:
    return _get_event_value(
        event_utils.get_event_pre_checkout_query_id,
        "pre checkout query identifier"
    )


def _get_event_value(getter: Callable[[Event], Any], name: str) -> Any:
    event = event_context.get()
    value = getter(event)

    if value is None:
        raise InvalidEventError(f"No {name} in event" + " {event!r}!", event=event)

    return value
