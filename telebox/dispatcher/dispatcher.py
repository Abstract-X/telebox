import logging
from typing import Optional, Union, NoReturn, Any
from dataclasses import dataclass
from threading import Thread, Lock
import time

from cachetools import TTLCache
import cherrypy

from telebox.telegram_bot.telegram_bot import TelegramBot
from telebox.telegram_bot.types.types.update import Update
from telebox.telegram_bot.types.types.message import Message
from telebox.telegram_bot.types.types.callback_query import CallbackQuery
from telebox.telegram_bot.errors import UnknownUpdateContentError, UnknownMessageContentError
from telebox.dispatcher.typing import Event
from telebox.dispatcher.media_group import MediaGroup
from telebox.dispatcher.event_queue import EventQueue, Event as Event_
from telebox.dispatcher.enums.event_type import EventType
from telebox.dispatcher.handlers.handlers.event import AbstractEventHandler
from telebox.dispatcher.handlers.handlers.error import AbstractErrorHandler
from telebox.dispatcher.filters.event_filter import AbstractEventBaseFilter
from telebox.dispatcher.filters.error_filter import AbstractErrorBaseFilter
from telebox.dispatcher.filters.event.none import NoneFilter
from telebox.dispatcher.filters.error.none import ErrorNoneFilter
from telebox.dispatcher.middlewares.middleware import Middleware
from telebox.dispatcher.rate_limiter import RateLimiter
from telebox.dispatcher.server_root import ServerRoot
from telebox.dispatcher.errors import DispatcherError
from telebox.utils.thread_pool import ThreadPool
from telebox.utils.not_set import NotSet
from telebox.context.vars import (
    event_context,
    event_handler_context,
    error_handler_context
)


logger = logging.getLogger(__name__)
_MEDIA_GROUP_GATHERING_DELAY_SECS = 0.1


@dataclass
class EventHandler:
    handler: AbstractEventHandler
    filter: AbstractEventBaseFilter
    rate_limiter: Optional[RateLimiter] = None
    calls: Optional[TTLCache] = None


@dataclass
class ErrorHandler:
    handler: AbstractErrorHandler
    filter: AbstractErrorBaseFilter


@dataclass
class CallState:
    is_first: bool


class TimeContainer:

    def __init__(self, initial_item: Any):
        self.items = [initial_item]
        self.time = time.monotonic()

    def add(self, item: Any) -> None:
        self.items.append(item)
        self.time = time.monotonic()


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
        self._media_group_gathering_thread: Optional[Thread] = None
        self._media_group_messages: dict[str, TimeContainer] = {}
        self._media_group_message_lock = Lock()

    def add_message_handler(
        self,
        handler: AbstractEventHandler,
        filter_: Optional[AbstractEventBaseFilter] = None,
        rate_limiter: Union[RateLimiter, None, NotSet] = NotSet()
    ) -> None:
        self._add_event_handler(handler, EventType.MESSAGE, filter_, rate_limiter)

    def add_edited_message_handler(
        self,
        handler: AbstractEventHandler,
        filter_: Optional[AbstractEventBaseFilter] = None,
        rate_limiter: Union[RateLimiter, None, NotSet] = NotSet()
    ) -> None:
        self._add_event_handler(handler, EventType.EDITED_MESSAGE, filter_, rate_limiter)

    def add_media_group_handler(
        self,
        handler: AbstractEventHandler,
        filter_: Optional[AbstractEventBaseFilter] = None,
        rate_limiter: Union[RateLimiter, None, NotSet] = NotSet()
    ) -> None:
        self._add_event_handler(handler, EventType.MEDIA_GROUP, filter_, rate_limiter)

    def add_channel_post_handler(
        self,
        handler: AbstractEventHandler,
        filter_: Optional[AbstractEventBaseFilter] = None
    ) -> None:
        self._add_event_handler(handler, EventType.CHANNEL_POST, filter_, None)

    def add_edited_channel_post_handler(
        self,
        handler: AbstractEventHandler,
        filter_: Optional[AbstractEventBaseFilter] = None
    ) -> None:
        self._add_event_handler(handler, EventType.EDITED_CHANNEL_POST, filter_, None)

    def add_inline_query_handler(
        self,
        handler: AbstractEventHandler,
        filter_: Optional[AbstractEventBaseFilter] = None,
        rate_limiter: Union[RateLimiter, None, NotSet] = NotSet()
    ) -> None:
        self._add_event_handler(handler, EventType.INLINE_QUERY, filter_, rate_limiter)

    def add_chosen_inline_result_handler(
        self,
        handler: AbstractEventHandler,
        filter_: Optional[AbstractEventBaseFilter] = None,
        rate_limiter: Union[RateLimiter, None, NotSet] = NotSet()
    ) -> None:
        self._add_event_handler(handler, EventType.CHOSEN_INLINE_RESULT, filter_, rate_limiter)

    def add_callback_query_handler(
        self,
        handler: AbstractEventHandler,
        filter_: Optional[AbstractEventBaseFilter] = None,
        rate_limiter: Union[RateLimiter, None, NotSet] = NotSet()
    ) -> None:
        self._add_event_handler(handler, EventType.CALLBACK_QUERY, filter_, rate_limiter)

    def add_shipping_query_handler(
        self,
        handler: AbstractEventHandler,
        filter_: Optional[AbstractEventBaseFilter] = None,
        rate_limiter: Union[RateLimiter, None, NotSet] = NotSet()
    ) -> None:
        self._add_event_handler(handler, EventType.SHIPPING_QUERY, filter_, rate_limiter)

    def add_pre_checkout_query_handler(
        self,
        handler: AbstractEventHandler,
        filter_: Optional[AbstractEventBaseFilter] = None,
        rate_limiter: Union[RateLimiter, None, NotSet] = NotSet()
    ) -> None:
        self._add_event_handler(handler, EventType.PRE_CHECKOUT_QUERY, filter_, rate_limiter)

    def add_poll_handler(
        self,
        handler: AbstractEventHandler,
        filter_: Optional[AbstractEventBaseFilter] = None
    ) -> None:
        self._add_event_handler(handler, EventType.POLL, filter_, None)

    def add_poll_answer_handler(
        self,
        handler: AbstractEventHandler,
        filter_: Optional[AbstractEventBaseFilter] = None,
        rate_limiter: Union[RateLimiter, None, NotSet] = NotSet()
    ) -> None:
        self._add_event_handler(handler, EventType.POLL_ANSWER, filter_, rate_limiter)

    def add_my_chat_member_handler(
        self,
        handler: AbstractEventHandler,
        filter_: Optional[AbstractEventBaseFilter] = None
    ) -> None:
        self._add_event_handler(handler, EventType.MY_CHAT_MEMBER, filter_, None)

    def add_chat_member_handler(
        self,
        handler: AbstractEventHandler,
        filter_: Optional[AbstractEventBaseFilter] = None
    ) -> None:
        self._add_event_handler(handler, EventType.CHAT_MEMBER, filter_, None)

    def add_chat_join_request_handler(
        self,
        handler: AbstractEventHandler,
        filter_: Optional[AbstractEventBaseFilter] = None
    ) -> None:
        self._add_event_handler(handler, EventType.CHAT_JOIN_REQUEST, filter_, None)

    def add_error_handler(
        self,
        handler: AbstractErrorHandler,
        filter_: Optional[AbstractErrorBaseFilter] = None
    ) -> None:
        if filter_ is None:
            filter_ = ErrorNoneFilter()

        self._error_handlers.append(
            ErrorHandler(
                handler=handler,
                filter=filter_
            )
        )

    def add_middleware(self, middleware: Middleware) -> None:
        self._middlewares.append(middleware)

    def run_polling(
        self,
        threads: int,
        *,
        timeout_secs: Union[int, float, None] = None,
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
        self._run_media_group_gathering_thread()
        self._run_thread_pool(threads)
        logger.info("Polling started.")

        try:
            while True:
                # noinspection PyBroadException
                try:
                    updates = self._bot.get_updates(
                        timeout_secs=timeout_secs,
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
            self._media_group_gathering_thread = None
            self._thread_pool = None
            self._polling_is_used = False

    def run_server(
        self,
        threads: int,
        webhook_path: Optional[str] = None,
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

        self._run_media_group_gathering_thread()
        self._run_thread_pool(threads)
        logger.info("Server started.")

        try:
            cherrypy.quickstart(
                root=ServerRoot(self._process_update),
                script_name=webhook_path.rstrip("/") if webhook_path else str()
            )
        finally:
            logger.info("Server stopped.")
            self._finish_update_processing()
            self._media_group_gathering_thread = None
            self._thread_pool = None
            self._server_is_used = False

    def drop_pending_updates(
        self,
        *,
        timeout_secs: Union[int, float, None] = None,
        with_delete_webhook: bool = True
    ) -> None:
        logger.debug("Dropping pending updates...")

        if with_delete_webhook:
            self._bot.delete_webhook(timeout_secs=timeout_secs, drop_pending_updates=True)
        else:
            updates = self._bot.get_updates(
                timeout_secs=timeout_secs,
                offset=-1
            )

            if updates:
                self._bot.get_updates(
                    timeout_secs=timeout_secs,
                    offset=updates[-1].update_id + 1
                )

        logger.info("Pending updates dropped.")

    def _add_event_handler(
        self,
        handler: AbstractEventHandler,
        event_type: EventType,
        filter_: Optional[AbstractEventBaseFilter] = None,
        rate_limiter: Union[RateLimiter, None, NotSet] = NotSet()
    ) -> None:
        if filter_ is None:
            filter_ = NoneFilter()

        if not filter_.check_event_type(event_type):
            raise DispatcherError(f"{event_type!r} is not supported by this filter!")

        if rate_limiter is NotSet():
            rate_limiter = self._default_rate_limiters.get(event_type)

        if rate_limiter is None:
            calls = None
        else:
            calls = TTLCache(maxsize=float("inf"), ttl=rate_limiter.secs)

        self._event_handlers[event_type].append(
            EventHandler(
                handler=handler,
                filter=filter_,
                rate_limiter=rate_limiter,
                calls=calls
            )
        )

    def _get_event_handler(
        self,
        event: Event,
        event_type: EventType
    ) -> Optional[EventHandler]:
        values = {}

        for i in self._event_handlers[event_type]:
            if (i.filter is None) or i.filter.get_result(event, event_type, values):
                return i

    def _get_error_handler(
        self,
        error: Exception,
        event: Event,
        event_type: EventType
    ) -> Optional[ErrorHandler]:
        values = {}

        for i in self._error_handlers:
            if (i.filter is None) or i.filter.get_result(error, event, event_type, values):
                return i

    def _run_media_group_gathering_thread(self) -> None:
        self._media_group_gathering_thread = Thread(
            target=self._run_media_group_gathering,
            daemon=True
        )
        self._media_group_gathering_thread.start()

    def _run_thread_pool(self, threads: int) -> None:
        self._thread_pool = ThreadPool(
            threads=threads,
            target=self._run_event_processing,
            args=(self._events,)
        )
        self._thread_pool.start()

    def _process_update(self, update: Update) -> None:
        logger.debug("Update received: %r.", update)

        try:
            event, content_type = update.content
        except UnknownUpdateContentError:
            logger.debug(
                "Update skipped because it contains an unknown content type: %r.",
                update
            )

            return

        event_type = EventType(content_type.value)

        if isinstance(event, Message):
            try:
                event.content  # noqa
            except UnknownMessageContentError:
                logger.debug(
                    "Event skipped because it contains an unknown content type: %r.",
                    event
                )

                return

            if event.media_group_id is not None:
                with self._media_group_message_lock:
                    if event.media_group_id in self._media_group_messages:
                        self._media_group_messages[event.media_group_id].add(event)
                    else:
                        self._media_group_messages[event.media_group_id] = TimeContainer(event)

                return

        if self._check_over_limit_event(event):
            logger.debug("Event from over limit chat dropped: %r.", event)
        else:
            logger.debug("Event added to queue: %r.", event)
            self._events.add_event(event, event_type)

    def _check_over_limit_event(self, event: Event) -> bool:
        return (
            self._drop_over_limit_events
            and isinstance(event, (Message, CallbackQuery, MediaGroup))
            and event.chat_id in self._bot.over_limit_chat_ids
        )

    def _finish_update_processing(self) -> None:
        logger.info("Update processing finishing...")
        self._events.wait_events()
        logger.info("Update processing finished.")

    def _run_media_group_gathering(self) -> NoReturn:
        while True:
            with self._media_group_message_lock:
                for i in tuple(self._media_group_messages):
                    if (time.monotonic() - self._media_group_messages[i].time) > 0.1:
                        event = MediaGroup(self._media_group_messages[i].items)
                        del self._media_group_messages[i]

                        if self._check_over_limit_event(event):
                            logger.debug("Event from over limit chat dropped: %r.", event)
                        else:
                            logger.debug("Event added to queue: %r.", event)
                            self._events.add_event(event, EventType.MEDIA_GROUP)

            time.sleep(_MEDIA_GROUP_GATHERING_DELAY_SECS)

    def _run_event_processing(self, events: EventQueue) -> NoReturn:
        while True:
            event_context_token = event_handler_context_token = error_handler_context_token = None
            event = events.get_event()

            # noinspection PyBroadException
            try:
                logger.debug("Event processing started: %r.", event)
                event_context_token = event_context.set(event.event)

                for i in self._middlewares:
                    i.pre_process_event(event.event, event.event_type)

                event_handler = self._get_event_handler(
                    event=event.event,
                    event_type=event.event_type
                )

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

                        error_handler = self._get_error_handler(
                            error=error,
                            event=event.event,
                            event_type=event.event_type
                        )

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
                logger.debug("Event processing finished: %r.", event)


def _process_rate_limiting(event: Event_, handler: EventHandler) -> bool:
    if handler.rate_limiter is not None:
        if event.user_id not in handler.calls:
            handler.calls[event.user_id] = CallState(is_first=True)
        else:
            if handler.calls[event.user_id].is_first:
                handler.calls[event.user_id].is_first = False
                handler.rate_limiter.process(event.event)

            return True

    return False
