from contextvars import ContextVar  # noqa


event_context_context = ContextVar("event_context_context")
event_context = ContextVar("event_context")
chat_id_context = ContextVar("chat_id_context")
user_id_context = ContextVar("user_id_context")
handler_context = ContextVar("handler_context")
error_handler_context = ContextVar("error_handler_context")
flow_id_context = ContextVar("flow_id_context")


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
