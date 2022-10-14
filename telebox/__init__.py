from .telegram_bot import TelegramBot, UpdateContentType, MessageContentType
from .dispatcher import (
    Dispatcher,
    EventType,
    AbstractHandler,
    AbstractEventHandler,
    AbstractErrorHandler,
    AbstractFilter,
    AbstractEventFilter,
    AbstractErrorFilter,
    Middleware,
    RateLimiter
)
from .state_machine import StateMachine, State, AbstractStateStorage
from .typing import Event
from .utils import (
    NamedSet,
    RequestTimeout,
    AbstractCallbackDataBuilder,
    ContextTelegramBot,
    ContextStateMachine,
    event_context,
    event_handler_context,
    error_handler_context
)


def _evaluate_type_annotations() -> None:
    from typing import get_type_hints

    from .telegram_bot.types.types.chat import Chat
    from .telegram_bot.types.types.message import Message

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
