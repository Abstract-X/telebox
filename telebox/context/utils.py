from typing import Optional

from telebox.context.vars import event_context
from telebox.dispatcher.utils import events as event_utils


def get_event_chat_id() -> Optional[int]:
    return event_utils.get_event_chat_id(
        event_context.get(),
        strictly=True
    )


def get_event_user_id() -> Optional[int]:
    return event_utils.get_event_user_id(
        event_context.get(),
        strictly=True
    )


def get_event_message_topic_id() -> Optional[int]:
    return event_utils.get_event_message_topic_id(
        event_context.get(),
        strictly=True
    )


def get_event_sender_chat_id() -> Optional[int]:
    return event_utils.get_event_sender_chat_id(
        event_context.get(),
        strictly=True
    )


def get_event_message_id() -> Optional[int]:
    return event_utils.get_event_message_id(
        event_context.get(),
        strictly=True
    )


def get_event_callback_query_id() -> str:
    return event_utils.get_event_callback_query_id(
        event_context.get(),
        strictly=True
    )


def get_event_inline_query_id() -> str:
    return event_utils.get_event_inline_query_id(
        event_context.get(),
        strictly=True
    )


def get_event_shipping_query_id() -> str:
    return event_utils.get_event_shipping_query_id(
        event_context.get(),
        strictly=True
    )


def get_event_pre_checkout_query_id() -> str:
    return event_utils.get_event_pre_checkout_query_id(
        event_context.get(),
        strictly=True
    )
