import logging
from typing import Optional, Union, NoReturn
from dataclasses import dataclass
from threading import Thread, Lock
from requests.exceptions import Timeout as RequestTimeoutError
import time

import cherrypy

from telebox.bot.bot import Bot
from telebox.bot.types.types.update import Update
from telebox.bot.types.types.message import Message
from telebox.dispatcher.typing import Event
from telebox.dispatcher.utils.media_group import MediaGroup
from telebox.dispatcher.utils.event_queue import EventQueue
from telebox.dispatcher.enums.event_type import EventType
from telebox.dispatcher.handlers.event import AbstractEventHandler
from telebox.dispatcher.handlers.error import AbstractErrorHandler
from telebox.dispatcher.filters.events.filter import AbstractEventBaseFilter
from telebox.dispatcher.filters.errors.filter import AbstractErrorBaseFilter
from telebox.dispatcher.filters.events.filters.none import NoneFilter
from telebox.dispatcher.filters.errors.filters.none import NoneErrorFilter
from telebox.dispatcher.middlewares.middleware import Middleware
from telebox.dispatcher.utils.rate_limiter.rate_limiter import RateLimiter
from telebox.dispatcher.utils.rate_limiter.rate_limit import RateLimit
from telebox.dispatcher.utils.media_group_container import MediaGroupContainer
from telebox.dispatcher.utils.server_root import ServerRoot
from telebox.dispatcher.utils.router import Router
from telebox.dispatcher.errors import DispatcherError
from telebox.utils.thread_pool import ThreadPool
from telebox.utils.not_set import NotSet, NOT_SET
from telebox.dispatcher.utils.events import get_event_chat_id
from telebox.context.vars import (
    event_context,
    event_handler_context,
    error_handler_context
)


logger = logging.getLogger(__name__)
_none_filter = NoneFilter()
_none_error_filter = NoneErrorFilter()
_MEDIA_GROUP_GATHERING_DELAY_SECS = 0.1
_DROPPED_UNKNOWN_UPDATE_MESSAGE = "Update dropped because it contains an unknown content type: %r."


@dataclass
class EventHandler:
    handler: AbstractEventHandler
    filter: AbstractEventBaseFilter
    rate_limiter: Optional[RateLimiter] = None

    @property
    def rate_limit(self) -> Optional[RateLimit]:
        return self.rate_limiter.limit if self.rate_limiter is not None else None


@dataclass
class ErrorHandler:
    handler: AbstractErrorHandler
    filter: AbstractErrorBaseFilter


class Dispatcher:

    def __init__(
        self,
        bot: Bot,
        *,
        drop_over_limit_events: bool = False,
        default_rate_limit: Optional[RateLimit] = None
    ):
        self._bot = bot
        self._drop_over_limit_events = drop_over_limit_events
        self._default_rate_limit = default_rate_limit
        self._polling_is_used = False
        self._server_is_used = False
        self._events = EventQueue()
        self._thread_pool: Optional[ThreadPool] = None
        self._event_handlers: dict[EventType, list[EventHandler]] = {i: [] for i in EventType}
        self._error_handlers: list[ErrorHandler] = []
        self._middlewares: list[Middleware] = []
        self.router = Router(self)
        self._media_group_gathering_thread: Optional[Thread] = None
        self._media_group_containers: dict[str, MediaGroupContainer] = {}
        self._media_group_message_lock = Lock()

    def add_message_handler(
        self,
        handler: AbstractEventHandler,
        filter_: Optional[AbstractEventBaseFilter] = None,
        rate_limit: Union[RateLimit, None, NotSet] = NOT_SET
    ) -> None:
        self._add_event_handler(handler, EventType.MESSAGE, filter_, rate_limit)

    def add_edited_message_handler(
        self,
        handler: AbstractEventHandler,
        filter_: Optional[AbstractEventBaseFilter] = None,
        rate_limit: Union[RateLimit, None, NotSet] = NOT_SET
    ) -> None:
        self._add_event_handler(handler, EventType.EDITED_MESSAGE, filter_, rate_limit)

    def add_channel_post_handler(
        self,
        handler: AbstractEventHandler,
        filter_: Optional[AbstractEventBaseFilter] = None,
        rate_limit: Union[RateLimit, None, NotSet] = NOT_SET
    ) -> None:
        self._add_event_handler(handler, EventType.CHANNEL_POST, filter_, rate_limit)

    def add_edited_channel_post_handler(
        self,
        handler: AbstractEventHandler,
        filter_: Optional[AbstractEventBaseFilter] = None,
        rate_limit: Union[RateLimit, None, NotSet] = NOT_SET
    ) -> None:
        self._add_event_handler(handler, EventType.EDITED_CHANNEL_POST, filter_, rate_limit)

    def add_media_group_handler(
        self,
        handler: AbstractEventHandler,
        filter_: Optional[AbstractEventBaseFilter] = None,
        rate_limit: Union[RateLimit, None, NotSet] = NOT_SET
    ) -> None:
        self._add_event_handler(handler, EventType.MEDIA_GROUP, filter_, rate_limit)

    def add_channel_media_group_handler(
        self,
        handler: AbstractEventHandler,
        filter_: Optional[AbstractEventBaseFilter] = None,
        rate_limit: Union[RateLimit, None, NotSet] = NOT_SET
    ) -> None:
        self._add_event_handler(handler, EventType.CHANNEL_MEDIA_GROUP, filter_, rate_limit)

    def add_inline_query_handler(
        self,
        handler: AbstractEventHandler,
        filter_: Optional[AbstractEventBaseFilter] = None,
        rate_limit: Union[RateLimit, None, NotSet] = NOT_SET
    ) -> None:
        self._add_event_handler(handler, EventType.INLINE_QUERY, filter_, rate_limit)

    def add_chosen_inline_result_handler(
        self,
        handler: AbstractEventHandler,
        filter_: Optional[AbstractEventBaseFilter] = None,
        rate_limit: Union[RateLimit, None, NotSet] = NOT_SET
    ) -> None:
        self._add_event_handler(handler, EventType.CHOSEN_INLINE_RESULT, filter_, rate_limit)

    def add_callback_query_handler(
        self,
        handler: AbstractEventHandler,
        filter_: Optional[AbstractEventBaseFilter] = None,
        rate_limit: Union[RateLimit, None, NotSet] = NOT_SET
    ) -> None:
        self._add_event_handler(handler, EventType.CALLBACK_QUERY, filter_, rate_limit)

    def add_shipping_query_handler(
        self,
        handler: AbstractEventHandler,
        filter_: Optional[AbstractEventBaseFilter] = None,
        rate_limit: Union[RateLimit, None, NotSet] = NOT_SET
    ) -> None:
        self._add_event_handler(handler, EventType.SHIPPING_QUERY, filter_, rate_limit)

    def add_pre_checkout_query_handler(
        self,
        handler: AbstractEventHandler,
        filter_: Optional[AbstractEventBaseFilter] = None,
        rate_limit: Union[RateLimit, None, NotSet] = NOT_SET
    ) -> None:
        self._add_event_handler(handler, EventType.PRE_CHECKOUT_QUERY, filter_, rate_limit)

    def add_poll_handler(
        self,
        handler: AbstractEventHandler,
        filter_: Optional[AbstractEventBaseFilter] = None
    ) -> None:
        self._add_event_handler(handler, EventType.POLL, filter_, None)

    def add_poll_answer_handler(
        self,
        handler: AbstractEventHandler,
        filter_: Optional[AbstractEventBaseFilter] = None
    ) -> None:
        self._add_event_handler(handler, EventType.POLL_ANSWER, filter_, None)

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
        filter_ = _get_error_filter(filter_)

        self._error_handlers.append(
            ErrorHandler(
                handler=handler,
                filter=filter_
            )
        )

    def add_middleware(self, middleware: Middleware) -> None:
        self._middlewares.append(middleware)

    def check_message_handler(
        self,
        handler: AbstractEventHandler,
        filter_: Optional[AbstractEventBaseFilter] = None,
        rate_limit: Union[RateLimit, None, NotSet] = NOT_SET
    ) -> bool:
        return self._check_event_handler(handler, EventType.MESSAGE, filter_, rate_limit)

    def check_edited_message_handler(
        self,
        handler: AbstractEventHandler,
        filter_: Optional[AbstractEventBaseFilter] = None,
        rate_limit: Union[RateLimit, None, NotSet] = NOT_SET
    ) -> bool:
        return self._check_event_handler(handler, EventType.EDITED_MESSAGE, filter_, rate_limit)

    def check_channel_post_handler(
        self,
        handler: AbstractEventHandler,
        filter_: Optional[AbstractEventBaseFilter] = None,
        rate_limit: Union[RateLimit, None, NotSet] = NOT_SET
    ) -> bool:
        return self._check_event_handler(handler, EventType.CHANNEL_POST, filter_, rate_limit)

    def check_edited_channel_post_handler(
        self,
        handler: AbstractEventHandler,
        filter_: Optional[AbstractEventBaseFilter] = None,
        rate_limit: Union[RateLimit, None, NotSet] = NOT_SET
    ) -> bool:
        return self._check_event_handler(
            handler,
            EventType.EDITED_CHANNEL_POST,
            filter_,
            rate_limit
        )

    def check_media_group_handler(
        self,
        handler: AbstractEventHandler,
        filter_: Optional[AbstractEventBaseFilter] = None,
        rate_limit: Union[RateLimit, None, NotSet] = NOT_SET
    ) -> bool:
        return self._check_event_handler(handler, EventType.MEDIA_GROUP, filter_, rate_limit)

    def check_channel_media_group_handler(
        self,
        handler: AbstractEventHandler,
        filter_: Optional[AbstractEventBaseFilter] = None,
        rate_limit: Union[RateLimit, None, NotSet] = NOT_SET
    ) -> bool:
        return self._check_event_handler(
            handler,
            EventType.CHANNEL_MEDIA_GROUP,
            filter_,
            rate_limit
        )

    def check_inline_query_handler(
        self,
        handler: AbstractEventHandler,
        filter_: Optional[AbstractEventBaseFilter] = None,
        rate_limit: Union[RateLimit, None, NotSet] = NOT_SET
    ) -> bool:
        return self._check_event_handler(handler, EventType.INLINE_QUERY, filter_, rate_limit)

    def check_chosen_inline_result_handler(
        self,
        handler: AbstractEventHandler,
        filter_: Optional[AbstractEventBaseFilter] = None,
        rate_limit: Union[RateLimit, None, NotSet] = NOT_SET
    ) -> bool:
        return self._check_event_handler(
            handler,
            EventType.CHOSEN_INLINE_RESULT,
            filter_,
            rate_limit
        )

    def check_callback_query_handler(
        self,
        handler: AbstractEventHandler,
        filter_: Optional[AbstractEventBaseFilter] = None,
        rate_limit: Union[RateLimit, None, NotSet] = NOT_SET
    ) -> bool:
        return self._check_event_handler(handler, EventType.CALLBACK_QUERY, filter_, rate_limit)

    def check_shipping_query_handler(
        self,
        handler: AbstractEventHandler,
        filter_: Optional[AbstractEventBaseFilter] = None,
        rate_limit: Union[RateLimit, None, NotSet] = NOT_SET
    ) -> bool:
        return self._check_event_handler(handler, EventType.SHIPPING_QUERY, filter_, rate_limit)

    def check_pre_checkout_query_handler(
        self,
        handler: AbstractEventHandler,
        filter_: Optional[AbstractEventBaseFilter] = None,
        rate_limit: Union[RateLimit, None, NotSet] = NOT_SET
    ) -> bool:
        return self._check_event_handler(
            handler,
            EventType.PRE_CHECKOUT_QUERY,
            filter_,
            rate_limit
        )

    def check_poll_handler(
        self,
        handler: AbstractEventHandler,
        filter_: Optional[AbstractEventBaseFilter] = None
    ) -> bool:
        return self._check_event_handler(handler, EventType.POLL, filter_, None)

    def check_poll_answer_handler(
        self,
        handler: AbstractEventHandler,
        filter_: Optional[AbstractEventBaseFilter] = None
    ) -> bool:
        return self._check_event_handler(handler, EventType.POLL_ANSWER, filter_, None)

    def check_my_chat_member_handler(
        self,
        handler: AbstractEventHandler,
        filter_: Optional[AbstractEventBaseFilter] = None
    ) -> bool:
        return self._check_event_handler(handler, EventType.MY_CHAT_MEMBER, filter_, None)

    def check_chat_member_handler(
        self,
        handler: AbstractEventHandler,
        filter_: Optional[AbstractEventBaseFilter] = None
    ) -> bool:
        return self._check_event_handler(handler, EventType.CHAT_MEMBER, filter_, None)

    def check_chat_join_request_handler(
        self,
        handler: AbstractEventHandler,
        filter_: Optional[AbstractEventBaseFilter] = None
    ) -> bool:
        return self._check_event_handler(handler, EventType.CHAT_JOIN_REQUEST, filter_, None)

    def check_error_handler(
        self,
        handler: AbstractErrorHandler,
        filter_: Optional[AbstractErrorBaseFilter] = None
    ) -> bool:
        filter_ = _get_error_filter(filter_)

        for i in self._error_handlers:
            if (i.handler is handler) and (i.filter is filter_):
                return True

        return False

    def check_middleware(self, middleware: Middleware) -> bool:
        for i in self._middlewares:
            if i is middleware:
                return True

        return False

    def run_polling(
        self,
        threads: int,
        *,
        delay_secs: Union[int, float] = 0,
        error_delay_secs: Union[int, float] = 5,
        limit: Optional[int] = None,
        timeout: Optional[int] = 10,
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
                        timeout_secs=timeout + 1 if timeout else None,
                        offset=offset_update_id,
                        limit=limit,
                        timeout=timeout,
                        allowed_updates=allowed_updates
                    )
                except RequestTimeoutError:
                    logger.error("Timeout for requesting updates has expired!")
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
        rate_limit: Union[RateLimit, None, NotSet] = NOT_SET
    ) -> None:
        filter_ = _get_event_filter(filter_)

        if not filter_.check_event_type(event_type):
            raise DispatcherError(f"{event_type!r} is not supported by this filter!")

        rate_limit = self._get_rate_limit(rate_limit)
        rate_limiter = RateLimiter(rate_limit) if rate_limit is not None else None
        self._event_handlers[event_type].append(
            EventHandler(
                handler=handler,
                filter=filter_,
                rate_limiter=rate_limiter
            )
        )

    def _check_event_handler(
        self,
        handler: AbstractEventHandler,
        event_type: EventType,
        filter_: Optional[AbstractEventBaseFilter] = None,
        rate_limit: Union[RateLimit, None, NotSet] = NOT_SET
    ) -> bool:
        filter_ = _get_event_filter(filter_)
        rate_limit = self._get_rate_limit(rate_limit)

        for i in self._event_handlers[event_type]:
            if (
                (i.handler is handler)
                and (i.filter is filter_)
                and (i.rate_limit is rate_limit)
            ):
                return True

        return False

    def _get_event_handler(self, event: Event, event_type: EventType) -> Optional[EventHandler]:
        results = {}

        for i in self._event_handlers[event_type]:
            if i.filter.get_result(event, results):
                return i

    def _get_error_handler(self, error: Exception, event: Event) -> Optional[ErrorHandler]:
        results = {}

        for i in self._error_handlers:
            if i.filter.get_result(error, event, results):
                return i

    def _get_rate_limit(
        self,
        rate_limit: Union[RateLimit, None, NotSet] = NOT_SET
    ) -> Optional[RateLimit]:
        return rate_limit if rate_limit is not NOT_SET else self._default_rate_limit

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
            args=(self._events,),
            with_barrier=True
        )
        self._thread_pool.start()

    def _process_update(self, update: Update) -> None:
        logger.debug("Update received: %r.", update)
        event = update.content

        if event is None:
            logger.debug(_DROPPED_UNKNOWN_UPDATE_MESSAGE, update)

            return

        if isinstance(event, Message):
            if event.content is None:
                logger.debug(_DROPPED_UNKNOWN_UPDATE_MESSAGE, update)

                return

            if event.media_group_id is not None:
                with self._media_group_message_lock:
                    if event.media_group_id not in self._media_group_containers:
                        self._media_group_containers[event.media_group_id] = MediaGroupContainer(
                            event=event,
                            event_type=EventType(update.content_type.value)
                        )
                    else:
                        self._media_group_containers[event.media_group_id].add_event(event)

                return

        if self._check_over_limit_event(event):
            logger.debug("Event from over limit chat dropped: %r.", event)
        else:
            logger.debug("Event added to queue: %r.", event)
            event_type = EventType(update.content_type.value)
            self._events.add_event(event, event_type)

    def _check_over_limit_event(self, event: Event) -> bool:
        return (
            self._drop_over_limit_events
            and get_event_chat_id(event) in self._bot.over_limit_chat_ids
        )

    def _finish_update_processing(self) -> None:
        logger.info("Finishing update processing...")
        self._events.wait_events()
        logger.info("Update processing finished.")

    def _run_media_group_gathering(self) -> NoReturn:
        while True:
            with self._media_group_message_lock:
                for media_group_id in tuple(self._media_group_containers):
                    if (time.monotonic() - self._media_group_containers[media_group_id].time) >= 1:
                        container = self._media_group_containers.pop(media_group_id)
                        event = MediaGroup(container.events)

                        if self._check_over_limit_event(event):
                            logger.debug("Event from over limit chat dropped: %r.", event)
                        else:
                            if container.event_type is EventType.MESSAGE:
                                event_type = EventType.MEDIA_GROUP
                            elif container.event_type is EventType.CHANNEL_POST:
                                event_type = EventType.CHANNEL_MEDIA_GROUP
                            else:
                                raise RuntimeError("Unknown message type!")

                            logger.debug("Event added to queue: %r.", event)
                            self._events.add_event(event, event_type)

            time.sleep(_MEDIA_GROUP_GATHERING_DELAY_SECS)

    def _run_event_processing(self, events: EventQueue) -> NoReturn:
        while True:
            event = events.get_event()

            try:
                logger.debug("Event processing started: %r.", event)
                event_context.set(event.event)

                for i in self._middlewares:
                    i.pre_process_event(event.event, event.event_type)

                event_handler = self._get_event_handler(event.event, event.event_type)

                if event_handler is None:
                    logger.debug("No handler found for event: %r.", event)
                    continue

                event_handler_context.set(event_handler.handler)

                if (
                    (event_handler.rate_limiter is not None)
                    and event_handler.rate_limiter.process_call(event.chat_id, event.user_id)
                ):
                    continue

                for i in self._middlewares:
                    i.process_event(event.event, event.event_type)

                event_handler.handler.process_event(event.event)

                for i in self._middlewares:
                    i.post_process_event(event.event, event.event_type)
            except Exception as error:
                # noinspection PyBroadException
                try:
                    for i in self._middlewares:
                        i.pre_process_error(error, event.event, event.event_type)

                    error_handler = self._get_error_handler(error, event.event)

                    if error_handler is None:
                        raise

                    error_handler_context.set(error_handler.handler)

                    for i in self._middlewares:
                        i.process_error(error, event.event, event.event_type)

                    error_handler.handler.process_error(error, event.event)

                    for i in self._middlewares:
                        i.post_process_error(error, event.event, event.event_type)
                except Exception:
                    logger.exception("An error occurred while processing an event!")
            finally:
                events.set_event_as_processed(event)
                logger.debug("Event processing finished: %r.", event)


def _get_event_filter(
    filter_: Optional[AbstractEventBaseFilter] = None
) -> AbstractEventBaseFilter:
    return filter_ if filter_ is not None else _none_filter


def _get_error_filter(
    filter_: Optional[AbstractErrorBaseFilter] = None
) -> AbstractErrorBaseFilter:
    return filter_ if filter_ is not None else _none_error_filter
