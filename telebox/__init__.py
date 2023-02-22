from .bot import Bot, get_bot, UpdateContentType, MessageContentType
from .dispatcher import (
    Dispatcher,
    Event,
    EventType,
    MediaGroup,
    MediaGroupContentType,
    AbstractEventHandler,
    AbstractErrorHandler,
    AbstractEventFilterFactory,
    AbstractEventFilter,
    AbstractEventBaseFilter,
    AbstractEventFilterCache,
    AbstractErrorFilterFactory,
    AbstractErrorFilter,
    AbstractErrorBaseFilter,
    AbstractErrorFilterCache,
    Middleware,
    RateLimit,
    Limit,
    Router,
    get_event_chat_id,
    get_event_user_id
)
from .state_machine import StateMachine, State, AbstractStateStorage
from .context import (
    ContextBot,
    ContextStateMachine,
    event_context,
    event_handler_context,
    error_handler_context
)
from .utils import (
    NotSet,
    NOT_SET,
    Group,
    AbstractCallbackDataBuilder,
    TaskExecutor,
    ThreadPool,
    Env,
    get_html_text,
    get_markdown_text
)


__all__ = [
    "Bot",
    "get_bot",
    "UpdateContentType",
    "MessageContentType",
    "Dispatcher",
    "Event",
    "EventType",
    "MediaGroup",
    "MediaGroupContentType",
    "AbstractEventHandler",
    "AbstractErrorHandler",
    "AbstractEventFilterFactory",
    "AbstractEventFilter",
    "AbstractEventBaseFilter",
    "AbstractEventFilterCache",
    "AbstractErrorFilterFactory",
    "AbstractErrorFilter",
    "AbstractErrorBaseFilter",
    "AbstractErrorFilterCache",
    "Middleware",
    "RateLimit",
    "Limit",
    "Router",
    "StateMachine",
    "State",
    "AbstractStateStorage",
    "ContextBot",
    "ContextStateMachine",
    "event_context",
    "event_handler_context",
    "error_handler_context",
    "NotSet",
    "NOT_SET",
    "Group",
    "AbstractCallbackDataBuilder",
    "TaskExecutor",
    "ThreadPool",
    "Env",
    "get_html_text",
    "get_markdown_text",
    "get_event_chat_id",
    "get_event_user_id"
]


def _evaluate_type_annotations() -> None:
    from typing import get_type_hints

    from .bot.types.types.chat import Chat
    from .bot.types.types.message import Message

    classes = (Chat, Message)
    mapping = {i.__name__: i for i in classes}

    for class_ in classes:
        class_.__annotations__ = get_type_hints(class_, mapping)

        for name, type_ in class_.__annotations__.items():
            class_.__dataclass_fields__[name].type = type_  # noqa


def _patch_requests_serializer() -> None:
    import warnings

    import ujson

    # https://github.com/psf/requests/issues/1595#issuecomment-30993198
    try:
        import requests.compat
    except ModuleNotFoundError:
        warnings.warn("Failed to set ujson in requests: the structure has changed!", stacklevel=2)
    else:
        requests.compat.json = ujson


_evaluate_type_annotations()
_patch_requests_serializer()
