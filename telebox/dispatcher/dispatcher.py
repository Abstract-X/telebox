import logging
from typing import Optional, Union, Literal
from dataclasses import dataclass
import time

from cachetools import TTLCache
import cherrypy

from telebox.telegram_bot.telegram_bot import TelegramBot
from telebox.telegram_bot.types.types.update import Update
from telebox.telegram_bot.types.types.message import Message
from telebox.telegram_bot.types.types.callback_query import CallbackQuery
from telebox.dispatcher.thread_pool import ThreadPool
from telebox.dispatcher.event_queue import EventQueue
from telebox.dispatcher.enums.event_type import EventType
from telebox.dispatcher.handlers.handlers.event import AbstractEventHandler
from telebox.dispatcher.handlers.handlers.error import AbstractErrorHandler
from telebox.dispatcher.filters.filter import (
    AbstractFilter,
    ExpressionType,
    AbstractExpression,
    NoneExpression,
    FilterExpression,
    InvertExpression,
    AndExpression,
    OrExpression
)
from telebox.dispatcher.filters.event_filter import AbstractEventFilter
from telebox.dispatcher.filters.error_filter import AbstractErrorFilter
from telebox.dispatcher.middlewares.middleware import Middleware
from telebox.dispatcher.rate_limiter import RateLimiter
from telebox.dispatcher.server_root import ServerRoot
from telebox.dispatcher.errors import DispatcherError
from telebox.utils.not_set import NotSet
from telebox.utils.request_timeout import RequestTimeout
from telebox.typing import Event
from telebox.utils.context.vars import (
    event_context,
    event_handler_context,
    error_handler_context
)


@dataclass
class EventHandler:
    handler: AbstractEventHandler
    filter: AbstractExpression
    rate_limiter: Optional[RateLimiter] = None
    calls: Optional[TTLCache] = None


@dataclass
class ErrorHandler:
    handler: AbstractErrorHandler
    filter: AbstractExpression


@dataclass
class CallState:
    is_first: bool


logger = logging.getLogger(__name__)
EventFilter = Union[AbstractEventFilter, AbstractExpression, None]
ErrorFilter = Union[AbstractErrorFilter, AbstractExpression, None]


class Dispatcher:

    def __init__(
        self,
        bot: TelegramBot,
        *,
        drop_over_limit_events: bool = False,
        default_rate_limiters: Optional[dict[EventType, RateLimiter]] = None
    ):
        self._bot = bot
        self._drop_over_limit_events = drop_over_limit_events
        self._default_rate_limiters = default_rate_limiters or {}
        self._polling_is_used = False
        self._server_is_used = False
        self._events = EventQueue()
        self._thread_pool: Optional[ThreadPool] = None
        self._event_handlers: dict[EventType, list[EventHandler]] = {i: [] for i in EventType}
        self._error_handlers: list[ErrorHandler] = []
        self._middlewares: list[Middleware] = []

    def add_message_handler(
        self,
        handler: AbstractEventHandler,
        filter_: EventFilter = None,
        rate_limiter: Union[RateLimiter, None, NotSet] = NotSet()
    ) -> None:
        self._add_event_handler(handler, EventType.MESSAGE, filter_, rate_limiter)

    def add_edited_message_handler(
        self,
        handler: AbstractEventHandler,
        filter_: EventFilter = None,
        rate_limiter: Union[RateLimiter, None, NotSet] = NotSet()
    ) -> None:
        self._add_event_handler(handler, EventType.EDITED_MESSAGE, filter_, rate_limiter)

    def add_channel_post_handler(
        self,
        handler: AbstractEventHandler,
        filter_: EventFilter = None
    ) -> None:
        self._add_event_handler(handler, EventType.CHANNEL_POST, filter_, None)

    def add_edited_channel_post_handler(
        self,
        handler: AbstractEventHandler,
        filter_: EventFilter = None
    ) -> None:
        self._add_event_handler(handler, EventType.EDITED_CHANNEL_POST, filter_, None)

    def add_inline_query_handler(
        self,
        handler: AbstractEventHandler,
        filter_: EventFilter = None,
        rate_limiter: Union[RateLimiter, None, NotSet] = NotSet()
    ) -> None:
        self._add_event_handler(handler, EventType.INLINE_QUERY, filter_, rate_limiter)

    def add_chosen_inline_result_handler(
        self,
        handler: AbstractEventHandler,
        filter_: EventFilter = None,
        rate_limiter: Union[RateLimiter, None, NotSet] = NotSet()
    ) -> None:
        self._add_event_handler(handler, EventType.CHOSEN_INLINE_RESULT, filter_, rate_limiter)

    def add_callback_query_handler(
        self,
        handler: AbstractEventHandler,
        filter_: EventFilter = None,
        rate_limiter: Union[RateLimiter, None, NotSet] = NotSet()
    ) -> None:
        self._add_event_handler(handler, EventType.CALLBACK_QUERY, filter_, rate_limiter)

    def add_shipping_query_handler(
        self,
        handler: AbstractEventHandler,
        filter_: EventFilter = None,
        rate_limiter: Union[RateLimiter, None, NotSet] = NotSet()
    ) -> None:
        self._add_event_handler(handler, EventType.SHIPPING_QUERY, filter_, rate_limiter)

    def add_pre_checkout_query_handler(
        self,
        handler: AbstractEventHandler,
        filter_: EventFilter = None,
        rate_limiter: Union[RateLimiter, None, NotSet] = NotSet()
    ) -> None:
        self._add_event_handler(handler, EventType.PRE_CHECKOUT_QUERY, filter_, rate_limiter)

    def add_poll_handler(
        self,
        handler: AbstractEventHandler,
        filter_: EventFilter = None
    ) -> None:
        self._add_event_handler(handler, EventType.POLL, filter_, None)

    def add_poll_answer_handler(
        self,
        handler: AbstractEventHandler,
        filter_: EventFilter = None,
        rate_limiter: Union[RateLimiter, None, NotSet] = NotSet()
    ) -> None:
        self._add_event_handler(handler, EventType.POLL_ANSWER, filter_, rate_limiter)

    def add_my_chat_member_handler(
        self,
        handler: AbstractEventHandler,
        filter_: EventFilter = None
    ) -> None:
        self._add_event_handler(handler, EventType.MY_CHAT_MEMBER, filter_, None)

    def add_chat_member_handler(
        self,
        handler: AbstractEventHandler,
        filter_: EventFilter = None
    ) -> None:
        self._add_event_handler(handler, EventType.CHAT_MEMBER, filter_, None)

    def add_chat_join_request_handler(
        self,
        handler: AbstractEventHandler,
        filter_: EventFilter = None
    ) -> None:
        self._add_event_handler(handler, EventType.CHAT_JOIN_REQUEST, filter_, None)

    def add_error_handler(
        self,
        handler: AbstractErrorHandler,
        filter_: ErrorFilter = None
    ) -> None:
        self._error_handlers.append(
            ErrorHandler(
                handler=handler,
                filter=_get_expression(filter_)
            )
        )

    def add_middleware(self, middleware: Middleware) -> None:
        self._middlewares.append(middleware)

    def run_polling(
        self,
        threads: int,
        *,
        request_timeout: Optional[RequestTimeout] = None,
        delay_secs: Union[int, float] = 0.2,
        error_delay_secs: Union[int, float] = 5.0,
        limit: Optional[int] = None,
        timeout: Optional[int] = None,
        allowed_updates: Optional[list[str]] = None
    ) -> None:
        if self._polling_is_used:
            raise DispatcherError("Polling cannot be run twice!")

        if self._server_is_used:
            raise DispatcherError("Polling cannot be run while the server is used!")

        if delay_secs < 0:
            raise ValueError("Delay seconds cannot be negative!")

        if error_delay_secs < 0:
            raise ValueError("Error delay seconds cannot be negative!")

        self._polling_is_used = True
        logger.debug("Polling is starting...")
        offset_update_id = None
        self._run_thread_pool(threads)
        logger.info("Polling started.")

        try:
            while True:
                # noinspection PyBroadException
                try:
                    updates = self._bot.get_updates(
                        request_timeout=request_timeout,
                        offset=offset_update_id,
                        limit=limit,
                        timeout=timeout,
                        allowed_updates=allowed_updates
                    )
                except Exception:
                    logger.exception("An error occurred while receiving updates!")
                    time.sleep(error_delay_secs)
                else:
                    for i in updates:
                        self._process_update(i)

                    if updates:
                        offset_update_id = updates[-1].update_id + 1

                    time.sleep(delay_secs)
        except KeyboardInterrupt:
            logger.info("Polling stopped.")
            self._finish_update_processing()
            self._polling_is_used = False

    def run_server(
        self,
        threads: int,
        webhook_path: str = "",
        *,
        host: str = "0.0.0.0",
        port: int = 443,
        ssl_certificate_path: Optional[str] = None,
        ssl_private_key_path: Optional[str] = None
    ) -> None:
        if self._server_is_used:
            raise DispatcherError("Server cannot be run twice!")

        if self._polling_is_used:
            raise DispatcherError("Server cannot be run while polling is used!")

        self._server_is_used = True
        logger.debug("Server is starting...")
        cherrypy.config.update({
            "server.socket_host": host,
            "server.socket_port": port,
            'environment': 'production',
            "engine.autoreload.on": False
        })

        if (ssl_certificate_path is not None) and (ssl_private_key_path is not None):
            cherrypy.config.update({
                "server.ssl_module": "builtin",
                "server.ssl_certificate": ssl_certificate_path,
                "server.ssl_private_key": ssl_private_key_path,
            })

        self._run_thread_pool(threads)
        logger.info("Server started.")

        try:
            cherrypy.quickstart(
                root=ServerRoot(self._process_update),
                script_name=webhook_path
            )
        finally:
            logger.info("Server stopped.")
            self._finish_update_processing()
            self._server_is_used = False

    def drop_pending_updates(
        self,
        *,
        request_timeout: Optional[RequestTimeout] = None,
        with_delete_webhook: bool = True
    ) -> None:
        logger.debug("Dropping pending updates...")

        if with_delete_webhook:
            self._bot.delete_webhook(request_timeout=request_timeout, drop_pending_updates=True)
        else:
            updates = self._bot.get_updates(
                request_timeout=request_timeout,
                offset=-1
            )

            if updates:
                self._bot.get_updates(
                    request_timeout=request_timeout,
                    offset=updates[-1].update_id + 1
                )

        logger.info("Pending updates dropped.")

    def _add_event_handler(
        self,
        handler: AbstractEventHandler,
        event_type: EventType,
        filter_: EventFilter = None,
        rate_limiter: Union[RateLimiter, None, NotSet] = NotSet()
    ) -> None:
        if rate_limiter is NotSet():
            rate_limiter = self._default_rate_limiters.get(event_type)

        if rate_limiter is None:
            calls = None
        else:
            calls = TTLCache(maxsize=float("inf"), ttl=rate_limiter.secs)

        self._event_handlers[event_type].append(
            EventHandler(
                handler=handler,
                filter=_get_expression(filter_),
                rate_limiter=rate_limiter,
                calls=calls
            )
        )

    def _get_event_handler(
        self,
        event: Event,
        event_type: EventType
    ) -> Optional[EventHandler]:
        return _get_handler(self._event_handlers[event_type], (event,))

    def _get_error_handler(
        self,
        error: Exception,
        event: Event
    ) -> Optional[ErrorHandler]:
        return _get_handler(self._error_handlers, (error, event))

    def _run_thread_pool(self, threads: int) -> None:
        self._thread_pool = ThreadPool(
            threads=threads,
            target=self._run_event_processing,
            args=(self._events,)
        )
        self._thread_pool.start()

    def _process_update(self, update: Update) -> None:
        logger.debug("Update received: %r.", update)
        event, event_type = update.content

        if (
            self._drop_over_limit_events
            and isinstance(event, (Message, CallbackQuery))
            and event.chat_id in self._bot.over_limit_chat_ids
        ):
            logger.debug("Event from over limit chat dropped: %r.", event)
        else:
            logger.debug("Event added to queue: %r.", event)
            self._events.add_event(event, event_type)

    def _finish_update_processing(self) -> None:
        logger.info("Update processing finishing...")
        self._events.wait_event_processing()
        self._thread_pool = None
        logger.info("Update processing finished.")

    def _run_event_processing(self, events: EventQueue) -> None:
        while True:
            event_context_token = event_handler_context_token = error_handler_context_token = None
            event = events.get_event()

            # noinspection PyBroadException
            try:
                logger.debug("Event processing started: %r.", event.event)
                event_context_token = event_context.set(event)

                for i in self._middlewares:
                    i.pre_process_event(event.event, event.event_type)

                event_handler = self._get_event_handler(event.event, event.event_type)

                if event_handler is not None:
                    event_handler_context_token = event_handler_context.set(event_handler.handler)

                    if _process_rate_limiting(event, event_handler):
                        continue

                    for i in self._middlewares:
                        i.process_event(event.event, event.event_type)

                    try:
                        event_handler.handler.process(event.event)
                    except Exception as error:
                        for i in self._middlewares:
                            i.pre_process_error(error, event.event, event.event_type)

                        error_handler = self._get_error_handler(error, event.event)

                        if error_handler is None:
                            raise

                        error_handler_context_token = error_handler_context.set(
                            error_handler.handler
                        )

                        for i in self._middlewares:
                            i.process_error(error, event.event, event.event_type)

                        try:
                            error_handler.handler.process(error, event.event, event.event_type)
                        finally:
                            for i in self._middlewares:
                                i.post_process_error(error, event.event, event.event_type)
                    finally:
                        for i in self._middlewares:
                            i.post_process_event(event.event, event.event_type)
                else:
                    logger.warning("No handler found for event: %r.", event)
            except Exception:
                logger.exception("An error occurred while processing an event!")
            finally:
                if event_context_token is not None:
                    event_context.reset(event_context_token)

                if event_handler_context_token is not None:
                    event_handler_context.reset(event_handler_context_token)

                if error_handler_context_token is not None:
                    error_handler_context.reset(error_handler_context_token)

                events.set_event_as_processed(event)
                logger.debug("Event processing finished: %r.", event.event)


def _process_rate_limiting(event: Event, handler: EventHandler) -> bool:
    if handler.rate_limiter is not None:
        if event.user_id not in handler.calls:
            handler.calls[event.user_id] = CallState(is_first=True)
        else:
            if handler.calls[event.user_id].is_first:
                handler.calls[event.user_id].is_first = False
                handler.rate_limiter.process(event.event)

            return True

    return False


def _get_handler(handlers: list, value_getting_args: tuple):
    filter_values = {}

    for i in handlers:
        result_getter = _EXPRESSION_RESULT_GETTERS[i.filter.get_type()]

        if result_getter(i.filter, filter_values, value_getting_args):
            return i


# noinspection PyUnusedLocal
def _get_none_expression_result(
    expression: NoneExpression,
    values: dict,
    value_getting_args: tuple
) -> Literal[True]:
    return True


def _get_filter_expression_result(
    expression: FilterExpression,
    values: dict,
    value_getting_args: tuple
) -> bool:
    filter_ = expression.value
    filter_type = type(filter_)

    try:
        value = values[filter_type]
    except KeyError:
        value = values[filter_type] = filter_.get_value(*value_getting_args)

    return filter_.check_value(value)


def _get_invert_expression_result(
    expression: InvertExpression,
    values: dict,
    value_getting_args: tuple
) -> bool:
    result_getter = _EXPRESSION_RESULT_GETTERS[expression.value.get_type()]

    return not result_getter(expression.value, values, value_getting_args)


def _get_and_expression_result(
    expression: AndExpression,
    values: dict,
    value_getting_args: tuple
) -> bool:
    return all(
        _EXPRESSION_RESULT_GETTERS[i.get_type()](i, values, value_getting_args)
        for i in expression
    )


def _get_or_expression_result(
    expression: OrExpression,
    values: dict,
    value_getting_args: tuple
) -> bool:
    return any(
        _EXPRESSION_RESULT_GETTERS[i.get_type()](i, values, value_getting_args)
        for i in expression
    )


_EXPRESSION_RESULT_GETTERS = {
    ExpressionType.NONE: _get_none_expression_result,
    ExpressionType.FILTER: _get_filter_expression_result,
    ExpressionType.INVERT: _get_invert_expression_result,
    ExpressionType.AND: _get_and_expression_result,
    ExpressionType.OR: _get_or_expression_result
}


def _get_expression(filter_) -> AbstractExpression:
    if filter_ is None:
        return NoneExpression()
    elif isinstance(filter_, AbstractFilter):
        return FilterExpression(filter_)
    elif isinstance(filter_, AbstractExpression):
        return filter_

    raise ValueError(f"Unknown filter type {filter_!r}!")
