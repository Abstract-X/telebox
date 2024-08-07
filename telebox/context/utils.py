from typing import Optional

from telebox.bot.types.types.chat_join_request import ChatJoinRequest
from telebox.context.vars import event_context
from telebox.dispatcher.utils import events as event_utils


def get_event_chat_id(
    *,
    strictly: bool = True,
    for_approve_chat_join_request: bool = False
) -> Optional[int]:
    event = event_context.get()

    if isinstance(event, ChatJoinRequest) and not for_approve_chat_join_request:
        return event_utils.get_event_user_id(event, strictly=True)

    return event_utils.get_event_chat_id(event=event, strictly=strictly)


def get_event_user_id(*, strictly: bool = True) -> Optional[int]:
    return event_utils.get_event_user_id(
        event_context.get(),
        strictly=strictly
    )


def get_event_message_topic_id(*, strictly: bool = True) -> Optional[int]:
    return event_utils.get_event_message_topic_id(
        event_context.get(),
        strictly=strictly
    )


def get_event_business_connection_id(*, strictly: bool = True) -> Optional[str]:
    return event_utils.get_business_connection_id(
        event_context.get(),
        strictly=strictly
    )


def get_event_sender_chat_id(*, strictly: bool = True) -> Optional[int]:
    return event_utils.get_event_sender_chat_id(
        event_context.get(),
        strictly=strictly
    )


def get_event_message_id(*, strictly: bool = True) -> Optional[int]:
    return event_utils.get_event_message_id(
        event_context.get(),
        strictly=strictly
    )


def get_event_callback_query_id(*, strictly: bool = True) -> str:
    return event_utils.get_event_callback_query_id(
        event_context.get(),
        strictly=strictly
    )


def get_event_inline_query_id(*, strictly: bool = True) -> str:
    return event_utils.get_event_inline_query_id(
        event_context.get(),
        strictly=strictly
    )


def get_event_shipping_query_id(*, strictly: bool = True) -> str:
    return event_utils.get_event_shipping_query_id(
        event_context.get(),
        strictly=strictly
    )


def get_event_pre_checkout_query_id(*, strictly: bool = True) -> str:
    return event_utils.get_event_pre_checkout_query_id(
        event_context.get(),
        strictly=strictly
    )
