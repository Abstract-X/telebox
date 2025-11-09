from typing import Any
from contextvars import ContextVar  # noqa


event_context = ContextVar("event_context")
handler_context = ContextVar("handler_context")
error_handler_context = ContextVar("error_handler_context")

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
    event = event_context.get()

    if not hasattr(event, _CONTEXT_ATTRS[name]):
        if not optional:
            raise ValueError(f"{name!r} is required!")

        return None

    return getattr(event, _CONTEXT_ATTRS[name])


class Context:
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


CONTEXT = Context(optional=False)
OPTIONAL_CONTEXT = Context(optional=True)
