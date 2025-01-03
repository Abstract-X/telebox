import logging
from typing import Optional, Union, NoReturn, Callable, TYPE_CHECKING
from pathlib import Path
from collections import deque
from queue import SimpleQueue as Queue
from threading import Thread, RLock, Condition, Event as ThreadingEvent
import contextlib
import time

from requests.exceptions import Timeout as RequestTimeoutError

if TYPE_CHECKING:
    from telebox.bot.bot import Bot
from telebox.bot.types.types.update import Update
from telebox.bot.types.types.message import Message
from telebox.bot.utils.converters import DataclassConverter
from telebox.dispatcher.typing import Event
from telebox.dispatcher.utils.media_group import MediaGroup
from telebox.dispatcher.enums.event_type import EventType
from telebox.dispatcher.enums.processing_status import ProcessingStatus
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
from telebox.dispatcher.utils.router import Router
from telebox.dispatcher.utils.events import (
    event_context,
    event_handler_context,
    error_handler_context,
    get_event_chat_id,
    get_event_user_id
)
from telebox.dispatcher.types.event_info import EventInfo
from telebox.dispatcher.types.event_handler_info import EventHandlerInfo
from telebox.dispatcher.types.error_handler_info import ErrorHandlerInfo
from telebox.dispatcher.types.aborting import ABORTING
from telebox.dispatcher.errors import DispatcherError
from telebox.utils.thread_pool import ThreadPool
from telebox.utils.not_set import NotSet, NOT_SET
from telebox.utils.serialization import get_deserialized_data


logger = logging.getLogger(__name__)
_none_filter = NoneFilter()
_none_error_filter = NoneErrorFilter()
_MEDIA_GROUP_GATHERING_DELAY_SECS = 0.1
_DROPPED_UNKNOWN_UPDATE_MESSAGE = "Update dropped because it contains an unknown content type: %r."
_EVENT_PROCESSING_LOG_TEMPLATES = {
    ProcessingStatus.PROCESSING: "Event processing finished: %r.",
    ProcessingStatus.ABORTED: "Event processing aborted: %r.",
    ProcessingStatus.HANDLER_NOT_FOUND: "No handler found for event: %r.",
    ProcessingStatus.RATE_LIMIT_EXCEEDED: "Rate limit exceeded for event: %r.",
    ProcessingStatus.ADDED_TO_CHAT_QUEUE: "Event added to chat queue: %r."
}


class Dispatcher:

    def __init__(
        self,
        bot: "Bot",
        *,
        rate_limit: Optional[RateLimit] = None,
        media_group_gathering_secs: Union[int, float] = 3
    ):
        self.bot = bot
        self._rate_limit = rate_limit
        self._media_group_gathering_secs = media_group_gathering_secs
        self._polling_is_used = False
        self._server_is_used = False
        self._events: deque[EventInfo] = deque()
        self._processing_chat_ids: set[int] = set()
        self._chat_queues: dict[int, Queue[EventInfo]] = {}
        self._unprocessed_events = 0
        self._event_lock = RLock()
        self._new_event_condition = Condition(self._event_lock)
        self._all_events_processed_condition = Condition(self._event_lock)
        self._thread_pool: Optional[ThreadPool] = None
        self._busy_threads = 0
        self._busy_thread_lock = RLock()
        self._event_handlers: dict[EventType, list[EventHandlerInfo]] = {i: [] for i in EventType}
        self._error_handlers: list[ErrorHandlerInfo] = []
        self._middlewares: list[Middleware] = []
        self.router = Router(self)
        self._media_group_gathering_thread: Optional[Thread] = None
        self._media_group_containers: dict[str, MediaGroupContainer] = {}
        self._media_group_message_lock = RLock()
        self._polling_stopping_event = ThreadingEvent()

    @property
    def polling_is_used(self) -> bool:
        return self._polling_is_used

    @property
    def server_is_used(self) -> bool:
        return self._server_is_used

    def add_message_handler(
        self,
        handler: AbstractEventHandler,
        filter_: Optional[AbstractEventBaseFilter] = None,
        rate_limit: Union[RateLimit, None, NotSet] = NOT_SET,
        with_chat_queue: bool = True
    ) -> None:
        self._add_event_handler(
            handler=handler,
            event_type=EventType.MESSAGE,
            filter_=filter_,
            rate_limit=rate_limit,
            with_chat_queue=with_chat_queue
        )

    def add_edited_message_handler(
        self,
        handler: AbstractEventHandler,
        filter_: Optional[AbstractEventBaseFilter] = None,
        rate_limit: Union[RateLimit, None, NotSet] = NOT_SET,
        with_chat_queue: bool = False
    ) -> None:
        self._add_event_handler(
            handler=handler,
            event_type=EventType.EDITED_MESSAGE,
            filter_=filter_,
            rate_limit=rate_limit,
            with_chat_queue=with_chat_queue
        )

    def add_business_connection_handler(
        self,
        handler: AbstractEventHandler,
        filter_: Optional[AbstractEventBaseFilter] = None
    ) -> None:
        self._add_event_handler(
            handler=handler,
            event_type=EventType.BUSINESS_CONNECTION,
            filter_=filter_
        )

    def add_business_message_handler(
        self,
        handler: AbstractEventHandler,
        filter_: Optional[AbstractEventBaseFilter] = None,
        rate_limit: Union[RateLimit, None, NotSet] = NOT_SET,
        with_chat_queue: bool = False
    ) -> None:
        self._add_event_handler(
            handler=handler,
            event_type=EventType.BUSINESS_MESSAGE,
            filter_=filter_,
            rate_limit=rate_limit,
            with_chat_queue=with_chat_queue
        )

    def add_edited_business_message_handler(
        self,
        handler: AbstractEventHandler,
        filter_: Optional[AbstractEventBaseFilter] = None,
        rate_limit: Union[RateLimit, None, NotSet] = NOT_SET,
        with_chat_queue: bool = False
    ) -> None:
        self._add_event_handler(
            handler=handler,
            event_type=EventType.EDITED_BUSINESS_MESSAGE,
            filter_=filter_,
            rate_limit=rate_limit,
            with_chat_queue=with_chat_queue
        )

    def add_deleted_business_messages_handler(
        self,
        handler: AbstractEventHandler,
        filter_: Optional[AbstractEventBaseFilter] = None
    ) -> None:
        self._add_event_handler(
            handler=handler,
            event_type=EventType.DELETED_BUSINESS_MESSAGES,
            filter_=filter_
        )

    def add_channel_post_handler(
        self,
        handler: AbstractEventHandler,
        filter_: Optional[AbstractEventBaseFilter] = None,
        rate_limit: Union[RateLimit, None, NotSet] = NOT_SET,
        with_chat_queue: bool = False
    ) -> None:
        self._add_event_handler(
            handler=handler,
            event_type=EventType.CHANNEL_POST,
            filter_=filter_,
            rate_limit=rate_limit,
            with_chat_queue=with_chat_queue
        )

    def add_edited_channel_post_handler(
        self,
        handler: AbstractEventHandler,
        filter_: Optional[AbstractEventBaseFilter] = None,
        rate_limit: Union[RateLimit, None, NotSet] = NOT_SET,
        with_chat_queue: bool = False
    ) -> None:
        self._add_event_handler(
            handler=handler,
            event_type=EventType.EDITED_CHANNEL_POST,
            filter_=filter_,
            rate_limit=rate_limit,
            with_chat_queue=with_chat_queue
        )

    def add_media_group_handler(
        self,
        handler: AbstractEventHandler,
        filter_: Optional[AbstractEventBaseFilter] = None,
        rate_limit: Union[RateLimit, None, NotSet] = NOT_SET,
        with_chat_queue: bool = True
    ) -> None:
        self._add_event_handler(
            handler=handler,
            event_type=EventType.MEDIA_GROUP,
            filter_=filter_,
            rate_limit=rate_limit,
            with_chat_queue=with_chat_queue
        )

    def add_channel_media_group_handler(
        self,
        handler: AbstractEventHandler,
        filter_: Optional[AbstractEventBaseFilter] = None,
        rate_limit: Union[RateLimit, None, NotSet] = NOT_SET,
        with_chat_queue: bool = False
    ) -> None:
        self._add_event_handler(
            handler=handler,
            event_type=EventType.CHANNEL_MEDIA_GROUP,
            filter_=filter_,
            rate_limit=rate_limit,
            with_chat_queue=with_chat_queue
        )

    def add_message_reaction_handler(
        self,
        handler: AbstractEventHandler,
        filter_: Optional[AbstractEventBaseFilter] = None,
        rate_limit: Union[RateLimit, None, NotSet] = NOT_SET,
        with_chat_queue: bool = False
    ) -> None:
        self._add_event_handler(
            handler=handler,
            event_type=EventType.MESSAGE_REACTION,
            filter_=filter_,
            rate_limit=rate_limit,
            with_chat_queue=with_chat_queue
        )

    def add_message_reaction_count_handler(
        self,
        handler: AbstractEventHandler,
        filter_: Optional[AbstractEventBaseFilter] = None,
        rate_limit: Union[RateLimit, None, NotSet] = NOT_SET,
        with_chat_queue: bool = False
    ) -> None:
        self._add_event_handler(
            handler=handler,
            event_type=EventType.MESSAGE_REACTION_COUNT,
            filter_=filter_,
            rate_limit=rate_limit,
            with_chat_queue=with_chat_queue
        )

    def add_inline_query_handler(
        self,
        handler: AbstractEventHandler,
        filter_: Optional[AbstractEventBaseFilter] = None,
        rate_limit: Union[RateLimit, None, NotSet] = NOT_SET
    ) -> None:
        self._add_event_handler(
            handler=handler,
            event_type=EventType.INLINE_QUERY,
            filter_=filter_,
            rate_limit=rate_limit
        )

    def add_chosen_inline_result_handler(
        self,
        handler: AbstractEventHandler,
        filter_: Optional[AbstractEventBaseFilter] = None,
        rate_limit: Union[RateLimit, None, NotSet] = NOT_SET
    ) -> None:
        self._add_event_handler(
            handler=handler,
            event_type=EventType.CHOSEN_INLINE_RESULT,
            filter_=filter_,
            rate_limit=rate_limit
        )

    def add_callback_query_handler(
        self,
        handler: AbstractEventHandler,
        filter_: Optional[AbstractEventBaseFilter] = None,
        rate_limit: Union[RateLimit, None, NotSet] = NOT_SET,
        with_chat_queue: bool = True
    ) -> None:
        self._add_event_handler(
            handler=handler,
            event_type=EventType.CALLBACK_QUERY,
            filter_=filter_,
            rate_limit=rate_limit,
            with_chat_queue=with_chat_queue
        )

    def add_shipping_query_handler(
        self,
        handler: AbstractEventHandler,
        filter_: Optional[AbstractEventBaseFilter] = None,
        rate_limit: Union[RateLimit, None, NotSet] = NOT_SET
    ) -> None:
        self._add_event_handler(
            handler=handler,
            event_type=EventType.SHIPPING_QUERY,
            filter_=filter_,
            rate_limit=rate_limit
        )

    def add_pre_checkout_query_handler(
        self,
        handler: AbstractEventHandler,
        filter_: Optional[AbstractEventBaseFilter] = None,
        rate_limit: Union[RateLimit, None, NotSet] = NOT_SET
    ) -> None:
        self._add_event_handler(
            handler=handler,
            event_type=EventType.PRE_CHECKOUT_QUERY,
            filter_=filter_,
            rate_limit=rate_limit
        )

    def add_poll_handler(
        self,
        handler: AbstractEventHandler,
        filter_: Optional[AbstractEventBaseFilter] = None
    ) -> None:
        self._add_event_handler(
            handler=handler,
            event_type=EventType.POLL,
            filter_=filter_
        )

    def add_poll_answer_handler(
        self,
        handler: AbstractEventHandler,
        filter_: Optional[AbstractEventBaseFilter] = None
    ) -> None:
        self._add_event_handler(
            handler=handler,
            event_type=EventType.POLL_ANSWER,
            filter_=filter_
        )

    def add_my_chat_member_handler(
        self,
        handler: AbstractEventHandler,
        filter_: Optional[AbstractEventBaseFilter] = None,
        with_chat_queue: bool = False
    ) -> None:
        self._add_event_handler(
            handler=handler,
            event_type=EventType.MY_CHAT_MEMBER,
            filter_=filter_,
            with_chat_queue=with_chat_queue
        )

    def add_chat_member_handler(
        self,
        handler: AbstractEventHandler,
        filter_: Optional[AbstractEventBaseFilter] = None,
        with_chat_queue: bool = False
    ) -> None:
        self._add_event_handler(
            handler=handler,
            event_type=EventType.CHAT_MEMBER,
            filter_=filter_,
            with_chat_queue=with_chat_queue
        )

    def add_chat_join_request_handler(
        self,
        handler: AbstractEventHandler,
        filter_: Optional[AbstractEventBaseFilter] = None
    ) -> None:
        self._add_event_handler(
            handler=handler,
            event_type=EventType.CHAT_JOIN_REQUEST,
            filter_=filter_
        )

    def add_chat_boost_handler(
        self,
        handler: AbstractEventHandler,
        filter_: Optional[AbstractEventBaseFilter] = None
    ) -> None:
        self._add_event_handler(
            handler=handler,
            event_type=EventType.CHAT_BOOST,
            filter_=filter_
        )

    def add_removed_chat_boost_handler(
        self,
        handler: AbstractEventHandler,
        filter_: Optional[AbstractEventBaseFilter] = None
    ) -> None:
        self._add_event_handler(
            handler=handler,
            event_type=EventType.REMOVED_CHAT_BOOST,
            filter_=filter_
        )

    def add_error_handler(
        self,
        handler: AbstractErrorHandler,
        filter_: Optional[AbstractErrorBaseFilter] = None
    ) -> None:
        filter_ = _get_error_filter(filter_)

        self._error_handlers.append(
            ErrorHandlerInfo(
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
        rate_limit: Optional[RateLimit] = None,
        with_chat_queue: bool = True
    ) -> bool:
        return self._check_event_handler(
            handler=handler,
            event_type=EventType.MESSAGE,
            filter_=filter_,
            rate_limit=rate_limit,
            with_chat_queue=with_chat_queue
        )

    def check_edited_message_handler(
        self,
        handler: AbstractEventHandler,
        filter_: Optional[AbstractEventBaseFilter] = None,
        rate_limit: Optional[RateLimit] = None,
        with_chat_queue: bool = False
    ) -> bool:
        return self._check_event_handler(
            handler=handler,
            event_type=EventType.EDITED_MESSAGE,
            filter_=filter_,
            rate_limit=rate_limit,
            with_chat_queue=with_chat_queue
        )

    def check_channel_post_handler(
        self,
        handler: AbstractEventHandler,
        filter_: Optional[AbstractEventBaseFilter] = None,
        rate_limit: Optional[RateLimit] = None,
        with_chat_queue: bool = False
    ) -> bool:
        return self._check_event_handler(
            handler=handler,
            event_type=EventType.CHANNEL_POST,
            filter_=filter_,
            rate_limit=rate_limit,
            with_chat_queue=with_chat_queue
        )

    def check_edited_channel_post_handler(
        self,
        handler: AbstractEventHandler,
        filter_: Optional[AbstractEventBaseFilter] = None,
        rate_limit: Optional[RateLimit] = None,
        with_chat_queue: bool = False
    ) -> bool:
        return self._check_event_handler(
            handler=handler,
            event_type=EventType.EDITED_CHANNEL_POST,
            filter_=filter_,
            rate_limit=rate_limit,
            with_chat_queue=with_chat_queue
        )

    def check_media_group_handler(
        self,
        handler: AbstractEventHandler,
        filter_: Optional[AbstractEventBaseFilter] = None,
        rate_limit: Optional[RateLimit] = None,
        with_chat_queue: bool = True
    ) -> bool:
        return self._check_event_handler(
            handler=handler,
            event_type=EventType.MEDIA_GROUP,
            filter_=filter_,
            rate_limit=rate_limit,
            with_chat_queue=with_chat_queue
        )

    def check_channel_media_group_handler(
        self,
        handler: AbstractEventHandler,
        filter_: Optional[AbstractEventBaseFilter] = None,
        rate_limit: Optional[RateLimit] = None,
        with_chat_queue: bool = False
    ) -> bool:
        return self._check_event_handler(
            handler=handler,
            event_type=EventType.CHANNEL_MEDIA_GROUP,
            filter_=filter_,
            rate_limit=rate_limit,
            with_chat_queue=with_chat_queue
        )

    def check_inline_query_handler(
        self,
        handler: AbstractEventHandler,
        filter_: Optional[AbstractEventBaseFilter] = None,
        rate_limit: Optional[RateLimit] = None
    ) -> bool:
        return self._check_event_handler(
            handler=handler,
            event_type=EventType.INLINE_QUERY,
            filter_=filter_,
            rate_limit=rate_limit
        )

    def check_chosen_inline_result_handler(
        self,
        handler: AbstractEventHandler,
        filter_: Optional[AbstractEventBaseFilter] = None,
        rate_limit: Optional[RateLimit] = None
    ) -> bool:
        return self._check_event_handler(
            handler=handler,
            event_type=EventType.CHOSEN_INLINE_RESULT,
            filter_=filter_,
            rate_limit=rate_limit
        )

    def check_callback_query_handler(
        self,
        handler: AbstractEventHandler,
        filter_: Optional[AbstractEventBaseFilter] = None,
        rate_limit: Optional[RateLimit] = None,
        with_chat_queue: bool = True
    ) -> bool:
        return self._check_event_handler(
            handler=handler,
            event_type=EventType.CALLBACK_QUERY,
            filter_=filter_,
            rate_limit=rate_limit,
            with_chat_queue=with_chat_queue
        )

    def check_shipping_query_handler(
        self,
        handler: AbstractEventHandler,
        filter_: Optional[AbstractEventBaseFilter] = None,
        rate_limit: Optional[RateLimit] = None
    ) -> bool:
        return self._check_event_handler(
            handler=handler,
            event_type=EventType.SHIPPING_QUERY,
            filter_=filter_,
            rate_limit=rate_limit
        )

    def check_pre_checkout_query_handler(
        self,
        handler: AbstractEventHandler,
        filter_: Optional[AbstractEventBaseFilter] = None,
        rate_limit: Optional[RateLimit] = None
    ) -> bool:
        return self._check_event_handler(
            handler=handler,
            event_type=EventType.PRE_CHECKOUT_QUERY,
            filter_=filter_,
            rate_limit=rate_limit
        )

    def check_poll_handler(
        self,
        handler: AbstractEventHandler,
        filter_: Optional[AbstractEventBaseFilter] = None
    ) -> bool:
        return self._check_event_handler(
            handler=handler,
            event_type=EventType.POLL,
            filter_=filter_
        )

    def check_poll_answer_handler(
        self,
        handler: AbstractEventHandler,
        filter_: Optional[AbstractEventBaseFilter] = None
    ) -> bool:
        return self._check_event_handler(
            handler=handler,
            event_type=EventType.POLL_ANSWER,
            filter_=filter_
        )

    def check_my_chat_member_handler(
        self,
        handler: AbstractEventHandler,
        filter_: Optional[AbstractEventBaseFilter] = None
    ) -> bool:
        return self._check_event_handler(
            handler=handler,
            event_type=EventType.MY_CHAT_MEMBER,
            filter_=filter_
        )

    def check_chat_member_handler(
        self,
        handler: AbstractEventHandler,
        filter_: Optional[AbstractEventBaseFilter] = None
    ) -> bool:
        return self._check_event_handler(
            handler=handler,
            event_type=EventType.CHAT_MEMBER,
            filter_=filter_
        )

    def check_chat_join_request_handler(
        self,
        handler: AbstractEventHandler,
        filter_: Optional[AbstractEventBaseFilter] = None
    ) -> bool:
        return self._check_event_handler(
            handler=handler,
            event_type=EventType.CHAT_JOIN_REQUEST,
            filter_=filter_
        )

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
        return middleware in self._middlewares

    def run_polling(
        self,
        min_threads: int = 5,
        max_threads: int = 25,
        *,
        error_delay_secs: Union[int, float] = 5,
        limit: Optional[int] = None,
        timeout: Optional[int] = 10,
        allowed_updates: Optional[list[str]] = None
    ) -> None:
        if self._polling_is_used:
            raise DispatcherError("Polling cannot be run twice!")

        if self._server_is_used:
            raise DispatcherError("Polling cannot be run while the server is used!")

        if error_delay_secs < 0:
            raise ValueError("Error delay seconds cannot be negative!")

        self._polling_is_used = True
        offset_update_id = None
        self._start_media_group_gathering_thread()
        self._start_thread_pool(min_threads, max_threads)
        logger.info("Polling started.")

        with contextlib.suppress(KeyboardInterrupt):
            while not self._polling_stopping_event.is_set():
                # noinspection PyBroadException
                try:
                    updates = self.bot.get_updates(
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

        self._polling_stopping_event.clear()
        logger.info("Polling stopped.")
        self._finish_update_processing()
        self._polling_is_used = False

    def stop_polling(self) -> None:
        if not self._polling_is_used:
            raise DispatcherError("Polling not running!")

        logger.info("Polling stopping...")
        self._polling_stopping_event.set()

    def run_server(
        self,
        min_threads: int = 5,
        max_threads: int = 25,
        *,
        host: str = "0.0.0.0",
        port: int = 443,
        path: Optional[str] = None,
        secret_token: Optional[str] = None,
        certificate_path: Union[str, Path, None] = None,
        private_key_path: Union[str, Path, None] = None
    ) -> None:
        try:
            import cherrypy
        except ImportError:
            raise ImportError(
                "To use server you need to install «CherryPy»:"
                "\npip install -U telebox[server]"
            ) from None

        if self._server_is_used:
            raise DispatcherError("Server cannot be run twice!")

        if self._polling_is_used:
            raise DispatcherError("Server cannot be run while polling is used!")

        self._server_is_used = True
        cherrypy.config.update({
            "server.socket_host": host,
            "server.socket_port": port,
            "server.shutdown_timeout": 1,
            "log.screen": False,
            "environment": "production"
        })

        if (certificate_path is not None) and (private_key_path is not None):
            cherrypy.config.update({
                "server.ssl_module": "builtin",
                "server.ssl_certificate": str(certificate_path),
                "server.ssl_private_key": str(private_key_path),
            })

        server_root = _get_server_root(
            update_processor=self._process_update,
            secret_token=secret_token
        )
        self._start_media_group_gathering_thread()
        self._start_thread_pool(min_threads, max_threads)
        path = (path or "").rstrip()

        if not path.startswith("/"):
            path = f"/{path}"

        cherrypy.log.error_log.propagate = False
        cherrypy.log.access_log.propagate = False
        logger.info("Server started.")
        cherrypy.tree.mount(server_root, path)
        cherrypy.engine.start()
        cherrypy.engine.block()
        logger.info("Server stopped.")
        self._finish_update_processing()
        self._server_is_used = False

    def stop_server(self) -> None:
        if not self._server_is_used:
            raise DispatcherError("Server not running!")

        import cherrypy

        logger.info("Server stopping...")
        cherrypy.engine.exit()

    def drop_pending_updates(
        self,
        *,
        timeout_secs: Union[int, float, None] = None,
        with_delete_webhook: bool = True
    ) -> None:
        logger.debug("Dropping pending updates...")

        if with_delete_webhook:
            self.bot.delete_webhook(timeout_secs=timeout_secs, drop_pending_updates=True)
        else:
            updates = self.bot.get_updates(
                timeout_secs=timeout_secs,
                offset=-1
            )

            if updates:
                self.bot.get_updates(
                    timeout_secs=timeout_secs,
                    offset=updates[-1].update_id + 1
                )

        logger.info("Pending updates dropped.")

    def _add_event_handler(
        self,
        handler: AbstractEventHandler,
        event_type: EventType,
        filter_: Optional[AbstractEventBaseFilter] = None,
        rate_limit: Union[RateLimit, None, NotSet] = None,
        with_chat_queue: bool = False
    ) -> None:
        filter_ = _get_event_filter(filter_)

        if not filter_.check_event_type(event_type):
            raise DispatcherError(f"{event_type!r} is not supported by this filter!")

        rate_limit = self._get_rate_limit(rate_limit)
        rate_limiter = RateLimiter(rate_limit) if rate_limit is not None else None
        self._event_handlers[event_type].append(
            EventHandlerInfo(
                handler=handler,
                filter=filter_,
                with_chat_queue=with_chat_queue,
                rate_limiter=rate_limiter
            )
        )

    def _check_event_handler(
        self,
        handler: AbstractEventHandler,
        event_type: EventType,
        filter_: Optional[AbstractEventBaseFilter] = None,
        rate_limit: Union[RateLimit, None, NotSet] = None,
        with_chat_queue: bool = False
    ) -> bool:
        filter_ = _get_event_filter(filter_)
        rate_limit = self._get_rate_limit(rate_limit)

        for i in self._event_handlers[event_type]:
            if (
                (i.handler is handler)
                and (i.filter is filter_)
                and (i.with_chat_queue is with_chat_queue)
                and (i.rate_limit is rate_limit)
            ):
                return True

        return False

    def _get_event_handler(self, event: Event, event_type: EventType) -> Optional[EventHandlerInfo]:
        results = {}

        for i in self._event_handlers[event_type]:
            if i.filter.get_result(event, results):
                return i

    def _get_error_handler(self, error: Exception, event: Event) -> Optional[ErrorHandlerInfo]:
        results = {}

        for i in self._error_handlers:
            if i.filter.get_result(error, event, results):
                return i

    def _get_rate_limit(
        self,
        rate_limit: Union[RateLimit, None, NotSet] = NOT_SET
    ) -> Optional[RateLimit]:
        return rate_limit if rate_limit is not NOT_SET else self._rate_limit

    def _start_media_group_gathering_thread(self) -> None:
        self._media_group_gathering_thread = Thread(
            target=self._run_media_group_gathering,
            daemon=True
        )
        self._media_group_gathering_thread.start()

    def _start_thread_pool(self, min_threads: int, max_threads: int) -> None:
        self._thread_pool = ThreadPool(
            min_threads=min_threads,
            max_threads=max_threads,
            target=self._run_event_processing,
            with_barrier=True
        )
        self._thread_pool.start_threads()

    def _process_update(self, update: Update) -> None:
        logger.debug("Update received: %r.", update)
        event = update.content

        if (
            (event is None)
            or (isinstance(event, Message) and (event.content is None))
        ):
            logger.debug(_DROPPED_UNKNOWN_UPDATE_MESSAGE, update)

            return

        event_type = EventType(update.content_type.value)

        if (
            (event_type in frozenset((EventType.MESSAGE, EventType.CHANNEL_POST)))
            and (event.media_group_id is not None)
        ):
            event: Message

            with self._media_group_message_lock:
                if event.media_group_id not in self._media_group_containers:
                    self._media_group_containers[event.media_group_id] = MediaGroupContainer(
                        event=event,
                        event_type=event_type
                    )
                else:
                    self._media_group_containers[event.media_group_id].add_event(event)

            return

        self._add_event_to_queue(
            EventInfo(
                event=event,
                event_type=event_type,
                chat_id=get_event_chat_id(event),
                user_id=get_event_user_id(event)
            )
        )

    def _finish_update_processing(self) -> None:
        logger.info("Finishing update processing...")
        self._wait_events()
        self._media_group_gathering_thread = None
        self._thread_pool = None
        logger.info("Update processing finished.")

    def _run_media_group_gathering(self) -> NoReturn:
        while True:
            with self._media_group_message_lock:
                for media_group_id in tuple(self._media_group_containers):
                    secs = time.monotonic() - self._media_group_containers[media_group_id].time

                    if secs > self._media_group_gathering_secs:
                        container = self._media_group_containers.pop(media_group_id)
                        event = MediaGroup(container.events)

                        if container.event_type is EventType.MESSAGE:
                            event_type = EventType.MEDIA_GROUP
                        elif container.event_type is EventType.CHANNEL_POST:
                            event_type = EventType.CHANNEL_MEDIA_GROUP
                        else:
                            raise RuntimeError(
                                f"Unknown message type {container.event_type!r}!"
                            )

                        self._add_event_to_queue(
                            EventInfo(
                                event=event,
                                event_type=event_type,
                                chat_id=get_event_chat_id(event),
                                user_id=get_event_user_id(event)
                            )
                        )

            time.sleep(_MEDIA_GROUP_GATHERING_DELAY_SECS)

    def _add_event_to_queue(self, event: EventInfo) -> None:
        with self._new_event_condition:
            self._events.append(event)
            self._unprocessed_events += 1
            logger.debug("Event added to queue: %r.", event.event)
            self._new_event_condition.notify()

    def _get_event_from_queue(self) -> EventInfo:
        with self._new_event_condition:
            while not self._events:
                self._new_event_condition.wait()

            return self._events.popleft()

    def _wait_events(self) -> None:
        with self._all_events_processed_condition:
            while self._unprocessed_events:
                self._all_events_processed_condition.wait()

    def _set_event_completion(self) -> None:
        with self._all_events_processed_condition:
            self._unprocessed_events -= 1

            if not self._unprocessed_events:
                self._all_events_processed_condition.notify_all()

    def _set_chat_event_completion(self, chat_id: int) -> None:
        with self._new_event_condition:
            chat_events = self._chat_queues.get(chat_id)

            if chat_events is None:
                self._processing_chat_ids.remove(chat_id)

                return

            next_event = chat_events.get_nowait()
            next_event.from_chat_queue = True

            if chat_events.empty():
                del self._chat_queues[chat_id]

            self._events.append(next_event)
            self._new_event_condition.notify()

    def _process_busy_threads(self) -> None:
        with self._busy_thread_lock:
            self._busy_threads += 1

            if (
                (self._busy_threads == self._thread_pool.threads)
                and (self._thread_pool.threads < self._thread_pool.max_threads)
            ):
                self._thread_pool.create_thread()
                logger.debug("Additional event processing thread created.")

    def _run_event_processing(self) -> NoReturn:
        while True:
            event = self._get_event_from_queue()
            logger.debug("Event processing started: %r.", event.event)

            try:
                event_context.set(event.event)
                self._process_busy_threads()
                event.busy_threads_processed = True

                if not event.middleware_pre_processed:
                    for i in self._middlewares:
                        result = i.pre_process_event(
                            event=event.event,
                            event_type=event.event_type
                        )

                        if result is ABORTING:
                            event.processing_status = ProcessingStatus.ABORTED
                            break

                    if event.processing_status is ProcessingStatus.ABORTED:
                        continue

                    event.middleware_pre_processed = True

                event_handler = self._get_event_handler(event.event, event.event_type)

                if event_handler is None:
                    event.processing_status = ProcessingStatus.HANDLER_NOT_FOUND
                    continue

                if event_handler.with_chat_queue and (event.chat_id is not None):
                    event.with_chat_queue = True

                    if not event.from_chat_queue:
                        with self._event_lock:
                            if event.chat_id in self._processing_chat_ids:
                                chat_events = self._chat_queues.get(event.chat_id)

                                if chat_events is None:
                                    chat_events = self._chat_queues[event.chat_id] = Queue()

                                chat_events.put_nowait(event)
                                event.processing_status = ProcessingStatus.ADDED_TO_CHAT_QUEUE
                                continue
                            else:
                                self._processing_chat_ids.add(event.chat_id)

                event_handler_context.set(event_handler.handler)

                if (
                    (event_handler.rate_limiter is not None)
                    and event_handler.rate_limiter.process_call(event.chat_id, event.user_id)
                ):
                    event.processing_status = ProcessingStatus.RATE_LIMIT_EXCEEDED
                    continue

                for i in self._middlewares:
                    result = i.process_event(
                        event=event.event,
                        event_type=event.event_type,
                        handler=event_handler.handler
                    )

                    if result is ABORTING:
                        event.processing_status = ProcessingStatus.ABORTED
                        break

                if event.processing_status is ProcessingStatus.ABORTED:
                    continue

                result = event_handler.handler.process_event(event.event)

                if result is ABORTING:
                    event.processing_status = ProcessingStatus.ABORTED
                    continue

                for i in self._middlewares:
                    result = i.post_process_event(
                        event=event.event,
                        event_type=event.event_type,
                        handler=event_handler.handler
                    )

                    if result is ABORTING:
                        event.processing_status = ProcessingStatus.ABORTED
                        break

                if event.processing_status is ProcessingStatus.ABORTED:
                    continue
            except Exception as error:
                event.processing_status = ProcessingStatus.ERROR_OCCURRED
                self._process_event_error(error, event)
            finally:
                if event.busy_threads_processed:
                    with self._busy_thread_lock:
                        self._busy_threads -= 1

                if event.processing_status is not ProcessingStatus.ERROR_OCCURRED:
                    logger.debug(
                        _EVENT_PROCESSING_LOG_TEMPLATES[event.processing_status],
                        event.event
                    )

                if event.processing_status is ProcessingStatus.ADDED_TO_CHAT_QUEUE:
                    event.processing_status = ProcessingStatus.PROCESSING
                    continue

                if event.with_chat_queue:
                    self._set_chat_event_completion(chat_id=event.chat_id)

                self._set_event_completion()

    def _process_event_error(self, error: Exception, event: EventInfo) -> None:
        # noinspection PyBroadException
        try:
            for i in self._middlewares:
                i.pre_process_error(error, event.event, event.event_type)

            error_handler = self._get_error_handler(error, event.event)

            if error_handler is None:
                raise error

            error_handler_context.set(error_handler.handler)

            for i in self._middlewares:
                i.process_error(error, event.event, event.event_type)

            error_handler.handler.process_error(error, event.event)

            for i in self._middlewares:
                i.post_process_error(error, event.event, event.event_type)
        except Exception:
            logger.exception("An error occurred while processing an event %r!", event.event)


def _get_event_filter(
    filter_: Optional[AbstractEventBaseFilter] = None
) -> AbstractEventBaseFilter:
    return filter_ if filter_ is not None else _none_filter


def _get_error_filter(
    filter_: Optional[AbstractErrorBaseFilter] = None
) -> AbstractErrorBaseFilter:
    return filter_ if filter_ is not None else _none_error_filter


def _get_server_root(
    update_processor: Callable[[Update], None],
    secret_token: Optional[str] = None
):
    import cherrypy

    class ServerRoot:

        def __init__(self):
            self._update_processor = update_processor
            self._secret_token = secret_token
            self._dataclass_converter = DataclassConverter()

        @cherrypy.expose
        def index(self) -> str:
            if self._secret_token is not None:
                secret_token_ = cherrypy.request.headers.get("X-Telegram-Bot-Api-Secret-Token")

                if secret_token_ != self._secret_token:
                    raise cherrypy.HTTPError(403)

            content_length = cherrypy.request.headers.get("Content-Length")

            if content_length is None:
                raise cherrypy.HTTPError(403)

            update = self._dataclass_converter.get_object(
                data=get_deserialized_data(
                    cherrypy.request.body.read(
                        int(content_length)
                    )
                ),
                class_=Update
            )
            self._update_processor(update)

            return ""

    return ServerRoot()
