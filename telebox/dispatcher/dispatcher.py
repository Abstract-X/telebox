import logging
from typing import Optional, Union, Literal
from dataclasses import dataclass
import time

from cachetools import TTLCache

from telebox.telegram_bot.telegram_bot import TelegramBot
from telebox.dispatcher.thread_pool import ThreadPool
from telebox.dispatcher.event_queue import EventQueue
from telebox.dispatcher.enums.event_type import EventType
from telebox.dispatcher.handlers.handlers.event import AbstractEventHandler
from telebox.dispatcher.handlers.handlers.error import AbstractErrorHandler
from telebox.dispatcher.handlers.filters.base.base import (
    AbstractFilter,
    ExpressionType,
    AbstractExpression,
    NoneExpression,
    FilterExpression,
    InvertExpression,
    AndExpression,
    OrExpression
)
from telebox.dispatcher.handlers.filters.base.event import AbstractEventFilter
from telebox.dispatcher.handlers.filters.base.error import AbstractErrorFilter
from telebox.dispatcher.rate_limiter import RateLimiter
from telebox.dispatcher.errors import PollingAlreadyStartedError
from telebox.utils import RequestTimeout, NotSetValue, NOT_SET_VALUE
from telebox.typing import Event


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
        default_rate_limiters: Optional[dict[EventType, RateLimiter]] = None
    ):
        self._bot = bot
        self._default_rate_limiters = default_rate_limiters or {}
        self._polling_is_started = False
        self._event_handlers: dict[EventType, list[EventHandler]] = {i: [] for i in EventType}
        self._error_handlers: list[ErrorHandler] = []

    def add_message_handler(
        self,
        handler: AbstractEventHandler,
        filter_: EventFilter = None,
        rate_limiter: Union[RateLimiter, None, NotSetValue] = NOT_SET_VALUE
    ) -> None:
        self._add_event_handler(handler, EventType.MESSAGE, filter_, rate_limiter)

    def add_edited_message_handler(
        self,
        handler: AbstractEventHandler,
        filter_: EventFilter = None,
        rate_limiter: Union[RateLimiter, None, NotSetValue] = NOT_SET_VALUE
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
        rate_limiter: Union[RateLimiter, None, NotSetValue] = NOT_SET_VALUE
    ) -> None:
        self._add_event_handler(handler, EventType.INLINE_QUERY, filter_, rate_limiter)

    def add_chosen_inline_result_handler(
        self,
        handler: AbstractEventHandler,
        filter_: EventFilter = None,
        rate_limiter: Union[RateLimiter, None, NotSetValue] = NOT_SET_VALUE
    ) -> None:
        self._add_event_handler(handler, EventType.CHOSEN_INLINE_RESULT, filter_, rate_limiter)

    def add_callback_query_handler(
        self,
        handler: AbstractEventHandler,
        filter_: EventFilter = None,
        rate_limiter: Union[RateLimiter, None, NotSetValue] = NOT_SET_VALUE
    ) -> None:
        self._add_event_handler(handler, EventType.CALLBACK_QUERY, filter_, rate_limiter)

    def add_shipping_query_handler(
        self,
        handler: AbstractEventHandler,
        filter_: EventFilter = None,
        rate_limiter: Union[RateLimiter, None, NotSetValue] = NOT_SET_VALUE
    ) -> None:
        self._add_event_handler(handler, EventType.SHIPPING_QUERY, filter_, rate_limiter)

    def add_pre_checkout_query_handler(
        self,
        handler: AbstractEventHandler,
        filter_: EventFilter = None,
        rate_limiter: Union[RateLimiter, None, NotSetValue] = NOT_SET_VALUE
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
        rate_limiter: Union[RateLimiter, None, NotSetValue] = NOT_SET_VALUE
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
        if self._polling_is_started:
            raise PollingAlreadyStartedError("Polling already started!")

        if delay_secs < 0:
            raise ValueError("Delay seconds cannot be negative!")

        if error_delay_secs < 0:
            raise ValueError("Error delay seconds cannot be negative!")

        logger.debug("Polling is starting...")
        self._polling_is_started = True
        offset_update_id = None
        events = EventQueue()
        thread_pool = ThreadPool(
            threads=threads,
            target=self._run_event_processing,
            args=(events,)
        )
        thread_pool.start()
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
                        logger.debug("Update received: %r.", i)
                        events.add_event(*i.content)

                    if updates:
                        offset_update_id = updates[-1].update_id + 1

                    time.sleep(delay_secs)
        except KeyboardInterrupt:
            logger.info("Polling stopped.")
            logger.info("Finishing processing updates...", )
            events.wait_event_processing()
            logger.info("Update processing finished.")
            self._polling_is_started = False

    def drop_pending_updates(
        self,
        *,
        request_timeout: Optional[RequestTimeout] = None
    ) -> None:
        logger.debug("Dropping pending updates...")
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
        rate_limiter: Union[RateLimiter, None, NotSetValue] = NOT_SET_VALUE
    ) -> None:
        if rate_limiter is NOT_SET_VALUE:
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

    def _run_event_processing(self, events: EventQueue) -> None:
        while True:
            event = events.get_event()

            try:
                logger.debug("Event processing started: %r.", event.event)
                event_handler = self._get_event_handler(event.event, event.event_type)

                if event_handler is not None:
                    if event_handler.rate_limiter is not None:
                        if event.user_id not in event_handler.calls:
                            event_handler.calls[event.user_id] = CallState(is_first=True)
                        elif event_handler.calls[event.user_id].is_first:
                            event_handler.calls[event.user_id].is_first = False
                            event_handler.rate_limiter.process(event.event)
                            continue
                        else:
                            continue

                    # noinspection PyBroadException
                    try:
                        try:
                            event_handler.handler.process(event.event)
                        except Exception as error:
                            error_handler = self._get_error_handler(
                                error=error,
                                event=event.event
                            )

                            if error_handler is None:
                                raise

                            error_handler.handler.process(error, event.event)
                    except Exception:
                        logger.exception("An error occurred while processing an update!")
            finally:
                events.set_event_as_processed(event)
                logger.debug("Event processing finished: %r.", event.event)


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
