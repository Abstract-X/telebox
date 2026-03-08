from typing import Any, Union, Optional
from contextvars import ContextVar  # noqa


event_context = ContextVar("event_context")
handler_context = ContextVar("handler_context")
error_handler_context = ContextVar("error_handler_context")
draft_context = ContextVar("draft_context")

_CONTEXT_ATTRS = {
    "chat_id": "chat_id",
    "user_id": "user_id",
    "message_thread_id": "message_thread_id",
    "business_connection_id": "business_connection_id",
    "sender_chat_id": "sender_chat_id",
    "message_id": "message_id",
    "callback_query_id": "id",
    "inline_query_id": "id",
    "shipping_query_id": "id",
    "pre_checkout_query_id": "id"
}


def get_event_value(name: str, optional: bool = False) -> Any:
    event = event_context.get(None)

    if event is None:
        if optional:
            return None

        raise LookupError(f"Unable to get {name!r}: event context is not set!")

    if not hasattr(event, _CONTEXT_ATTRS[name]):
        if not optional:
            raise ValueError(f"{name!r} is required!")

        return None

    return getattr(event, _CONTEXT_ATTRS[name])


class FromContext:
    __slots__ = ("optional",)
    __optional_instance = None
    __required_instance = None

    def __new__(cls, optional: bool):
        if optional:
            if cls.__optional_instance is None:
                cls.__optional_instance = super().__new__(cls)
                cls.__optional_instance.optional = True

            return cls.__optional_instance
        else:
            if cls.__required_instance is None:
                cls.__required_instance = super().__new__(cls)
                cls.__required_instance.optional = False

            return cls.__required_instance

    def __repr__(self):
        return f"<{type(self).__name__}>"

    def __bool__(self):
        return False


FROM_CONTEXT = FromContext(optional=False)
OPTIONAL_FROM_CONTEXT = FromContext(optional=True)


def get_chat_id_and_user_id(
    chat_id: Union[int, FromContext],
    user_id: Union[int, FromContext, None]
) -> tuple[int, Optional[int]]:
    if isinstance(chat_id, FromContext):
        chat_id = get_event_value("chat_id", optional=chat_id.optional)

    if isinstance(user_id, FromContext):
        user_id = get_event_value("user_id", optional=user_id.optional)

    return chat_id, user_id
