import logging
from typing import Optional, Union, NoReturn, Callable, TYPE_CHECKING
from pathlib import Path
from collections import deque
from queue import SimpleQueue as Queue
import threading
from threading import Thread, RLock, Condition, Event as ThreadingEvent
import contextlib
import time

from requests.exceptions import Timeout as RequestTimeoutError

if TYPE_CHECKING:
    from telebox.bot.bot import Bot
from telebox.bot.types.update import Update
from telebox.bot.types.message import Message
from telebox.bot.utils.converter import Converter
from telebox.dispatcher.utils.media_group import MediaGroup
from telebox.dispatcher.enums.event_type import EventType
from telebox.dispatcher.enums.processing_status import ProcessingStatus
from telebox.dispatcher.handlers.event import AbstractEventHandler
from telebox.dispatcher.handlers.error import AbstractErrorHandler
from telebox.dispatcher.filters.filter import AbstractBaseFilter
from telebox.dispatcher.filters.filters.none import NoneFilter
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
from telebox.utils.deps.deps import Deps
from telebox.utils.not_set import NotSet, NOT_SET
from telebox.utils.serialization import get_deserialized_data


logger = logging.getLogger(__name__)
_none_filter = NoneFilter()
_WORKER_WAITING_SECS = 60
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
        deps: Deps,
        *,
        min_workers: int = 10,
        max_workers: int = 100,
        rate_limit: Optional[RateLimit] = None,
        media_group_collecting_secs: Union[int, float] = 3
    ):
        self.bot = bot
        self._deps = deps
        self._min_workers = min_workers
        self._max_workers = max_workers
        self._rate_limit = rate_limit
        self._media_group_collecting_secs = media_group_collecting_secs
        self._polling_is_used = False
        self._server_is_used = False
        self._events: deque[EventInfo] = deque()
        self._processing_chat_ids: set[int] = set()
        self._chat_queues: dict[int, Queue[EventInfo]] = {}
        self._unprocessed_events = 0
        self._event_lock = RLock()
        self._new_event_condition = Condition(self._event_lock)
        self._all_events_processed_condition = Condition(self._event_lock)
        self._workers: dict[str, Thread] = {}
        self._worker_lock = RLock()
        self._worker_count = 0
        self._event_handlers: dict[EventType, list[EventHandlerInfo]] = {i: [] for i in EventType}
        self._error_handlers: list[ErrorHandlerInfo] = []
        self._middlewares: list[Middleware] = []
        self.router = Router(self)
        self._media_group_collector: Optional[Thread] = None
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
        filter_: Optional[AbstractBaseFilter] = None,
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
        filter_: Optional[AbstractBaseFilter] = None,
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
        filter_: Optional[AbstractBaseFilter] = None
    ) -> None:
        self._add_event_handler(
            handler=handler,
            event_type=EventType.BUSINESS_CONNECTION,
            filter_=filter_
        )

    def add_business_message_handler(
        self,
        handler: AbstractEventHandler,
        filter_: Optional[AbstractBaseFilter] = None,
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
        filter_: Optional[AbstractBaseFilter] = None,
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
        filter_: Optional[AbstractBaseFilter] = None
    ) -> None:
        self._add_event_handler(
            handler=handler,
            event_type=EventType.DELETED_BUSINESS_MESSAGES,
            filter_=filter_
        )

    def add_channel_post_handler(
        self,
        handler: AbstractEventHandler,
        filter_: Optional[AbstractBaseFilter] = None,
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
        filter_: Optional[AbstractBaseFilter] = None,
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
        filter_: Optional[AbstractBaseFilter] = None,
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
        filter_: Optional[AbstractBaseFilter] = None,
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
        filter_: Optional[AbstractBaseFilter] = None,
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
        filter_: Optional[AbstractBaseFilter] = None,
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
        filter_: Optional[AbstractBaseFilter] = None,
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
        filter_: Optional[AbstractBaseFilter] = None,
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
        filter_: Optional[AbstractBaseFilter] = None,
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
        filter_: Optional[AbstractBaseFilter] = None,
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
        filter_: Optional[AbstractBaseFilter] = None,
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
        filter_: Optional[AbstractBaseFilter] = None
    ) -> None:
        self._add_event_handler(
            handler=handler,
            event_type=EventType.POLL,
            filter_=filter_
        )

    def add_poll_answer_handler(
        self,
        handler: AbstractEventHandler,
        filter_: Optional[AbstractBaseFilter] = None
    ) -> None:
        self._add_event_handler(
            handler=handler,
            event_type=EventType.POLL_ANSWER,
            filter_=filter_
        )

    def add_my_chat_member_handler(
        self,
        handler: AbstractEventHandler,
        filter_: Optional[AbstractBaseFilter] = None,
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
        filter_: Optional[AbstractBaseFilter] = None,
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
        filter_: Optional[AbstractBaseFilter] = None
    ) -> None:
        self._add_event_handler(
            handler=handler,
            event_type=EventType.CHAT_JOIN_REQUEST,
            filter_=filter_
        )

    def add_chat_boost_handler(
        self,
        handler: AbstractEventHandler,
        filter_: Optional[AbstractBaseFilter] = None
    ) -> None:
        self._add_event_handler(
            handler=handler,
            event_type=EventType.CHAT_BOOST,
            filter_=filter_
        )

    def add_removed_chat_boost_handler(
        self,
        handler: AbstractEventHandler,
        filter_: Optional[AbstractBaseFilter] = None
    ) -> None:
        self._add_event_handler(
            handler=handler,
            event_type=EventType.REMOVED_CHAT_BOOST,
            filter_=filter_
        )

    def add_error_handler(
        self,
        handler: AbstractErrorHandler,
        error_type: type = Exception
    ) -> None:
        self._error_handlers.append(
            ErrorHandlerInfo(
                handler=handler,
                error_type=error_type
            )
        )

    def add_middleware(self, middleware: Middleware) -> None:
        self._middlewares.append(middleware)

    def check_message_handler(
        self,
        handler: AbstractEventHandler,
        filter_: Optional[AbstractBaseFilter] = None,
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
        filter_: Optional[AbstractBaseFilter] = None,
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
        filter_: Optional[AbstractBaseFilter] = None,
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
        filter_: Optional[AbstractBaseFilter] = None,
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
        filter_: Optional[AbstractBaseFilter] = None,
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
        filter_: Optional[AbstractBaseFilter] = None,
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
        filter_: Optional[AbstractBaseFilter] = None,
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
        filter_: Optional[AbstractBaseFilter] = None,
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
        filter_: Optional[AbstractBaseFilter] = None,
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
        filter_: Optional[AbstractBaseFilter] = None,
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
        filter_: Optional[AbstractBaseFilter] = None,
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
        filter_: Optional[AbstractBaseFilter] = None
    ) -> bool:
        return self._check_event_handler(
            handler=handler,
            event_type=EventType.POLL,
            filter_=filter_
        )

    def check_poll_answer_handler(
        self,
        handler: AbstractEventHandler,
        filter_: Optional[AbstractBaseFilter] = None
    ) -> bool:
        return self._check_event_handler(
            handler=handler,
            event_type=EventType.POLL_ANSWER,
            filter_=filter_
        )

    def check_my_chat_member_handler(
        self,
        handler: AbstractEventHandler,
        filter_: Optional[AbstractBaseFilter] = None
    ) -> bool:
        return self._check_event_handler(
            handler=handler,
            event_type=EventType.MY_CHAT_MEMBER,
            filter_=filter_
        )

    def check_chat_member_handler(
        self,
        handler: AbstractEventHandler,
        filter_: Optional[AbstractBaseFilter] = None
    ) -> bool:
        return self._check_event_handler(
            handler=handler,
            event_type=EventType.CHAT_MEMBER,
            filter_=filter_
        )

    def check_chat_join_request_handler(
        self,
        handler: AbstractEventHandler,
        filter_: Optional[AbstractBaseFilter] = None
    ) -> bool:
        return self._check_event_handler(
            handler=handler,
            event_type=EventType.CHAT_JOIN_REQUEST,
            filter_=filter_
        )

    def check_error_handler(
        self,
        handler: AbstractErrorHandler,
        error_type: type
    ) -> bool:
        for i in self._error_handlers:
            if (i.handler is handler) and (error_type is i.error_type):
                return True

        return False

    def check_middleware(self, middleware: Middleware) -> bool:
        return middleware in self._middlewares

    def run_polling(
        self,
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
        self._initialize_event_listening()
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
        *,
        host: str = "0.0.0.0",
        port: int = 443,
        path: Optional[str] = None,
        secret_token: Optional[str] = None,
        certificate_path: Union[str, Path, None] = None,
        private_key_path: Union[str, Path, None] = None
    ) -> None:
        try:
            import cherrypy  # noqa
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
        self._initialize_event_listening()
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

        import cherrypy  # noqa

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

    def _initialize_event_listening(self) -> None:
        self._create_media_group_collector()

        with self._worker_lock:
            for _ in range(self._min_workers):
                self._create_worker()

    def _add_event_handler(
        self,
        handler: AbstractEventHandler,
        event_type: EventType,
        filter_: Optional[AbstractBaseFilter] = None,
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
        filter_: Optional[AbstractBaseFilter] = None,
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

    def _get_event_handler(self, event: EventInfo) -> Optional[EventHandlerInfo]:
        filter_results: dict[AbstractBaseFilter, bool] = {}

        for i in self._event_handlers[event.event_type]:
            try:
                result = filter_results[i.filter]
            except KeyError:
                result = i.filter.get_result(event.event)
                filter_results[i.filter] = result

            if result:
                return i

    def _get_error_handler(self, error: Exception) -> Optional[ErrorHandlerInfo]:
        for i in self._error_handlers:
            if isinstance(error, i.error_type):
                return i

    def _get_rate_limit(
        self,
        rate_limit: Union[RateLimit, None, NotSet] = NOT_SET
    ) -> Optional[RateLimit]:
        return rate_limit if rate_limit is not NOT_SET else self._rate_limit

    def _create_media_group_collector(self) -> None:
        self._media_group_collector = Thread(
            target=self._run_media_group_collecting,
            daemon=True
        )
        self._media_group_collector.start()

    def _create_worker(self) -> None:
        self._worker_count += 1
        worker = Thread(
            target=self._run_event_processing,
            name=f"DispatcherWorker-{self._worker_count}",
            daemon=True
        )
        self._workers[worker.name] = worker
        logger.debug(
            "Worker %r started (workers: %r).",
            worker.name,
            len(self._workers)
        )
        worker.start()

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

    def _run_media_group_collecting(self) -> NoReturn:
        while True:
            with self._media_group_message_lock:
                for media_group_id in tuple(self._media_group_containers):
                    secs = time.monotonic() - self._media_group_containers[media_group_id].time

                    if secs > self._media_group_collecting_secs:
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

            time.sleep(0.1)

    def _add_event_to_queue(self, event: EventInfo) -> None:
        with self._new_event_condition:
            self._events.append(event)
            self._unprocessed_events += 1
            logger.debug(
                "Event added to queue: %r (events: %r).",
                event.event,
                len(self._events)
            )
            self._new_event_condition.notify()

            with self._worker_lock:
                if (
                    (self._unprocessed_events > len(self._workers))
                    and (len(self._workers) < self._max_workers)
                ):
                    self._create_worker()

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

    def _process_event(self, event: EventInfo) -> None:
        logger.debug("Event processing started: %r.", event.event)

        try:
            event_context.set(event.event)

            if not event.middleware_pre_processed:
                for i in self._middlewares:
                    result = i.pre_process_event(
                        deps=self._deps,
                        event=event.event,
                        event_type=event.event_type
                    )

                    if result is ABORTING:
                        event.processing_status = ProcessingStatus.ABORTED

                        return

                event.middleware_pre_processed = True

            event_handler = self._get_event_handler(event)

            if event_handler is None:
                event.processing_status = ProcessingStatus.HANDLER_NOT_FOUND

                return

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

                            return
                        else:
                            self._processing_chat_ids.add(event.chat_id)

            event_handler_context.set(event_handler.handler)

            if (
                (event_handler.rate_limiter is not None)
                and event_handler.rate_limiter.process_call(event.chat_id, event.user_id)
            ):
                event.processing_status = ProcessingStatus.RATE_LIMIT_EXCEEDED

                return

            for i in self._middlewares:
                result = i.process_event(
                    deps=self._deps,
                    event=event.event,
                    event_type=event.event_type,
                    handler=event_handler.handler
                )

                if result is ABORTING:
                    event.processing_status = ProcessingStatus.ABORTED

                    return

            result = event_handler.handler.process_event(
                deps=self._deps,
                event=event.event
            )

            if result is ABORTING:
                event.processing_status = ProcessingStatus.ABORTED

                return

            for i in self._middlewares:
                result = i.post_process_event(
                    deps=self._deps,
                    event=event.event,
                    event_type=event.event_type,
                    handler=event_handler.handler
                )

                if result is ABORTING:
                    event.processing_status = ProcessingStatus.ABORTED
                    break

            if event.processing_status is ProcessingStatus.ABORTED:
                return
        except Exception as error:
            event.processing_status = ProcessingStatus.ERROR_OCCURRED
            self._process_event_error(error, event)
        finally:
            if event.processing_status is not ProcessingStatus.ERROR_OCCURRED:
                logger.debug(
                    _EVENT_PROCESSING_LOG_TEMPLATES[event.processing_status],
                    event.event
                )

            if event.processing_status is ProcessingStatus.ADDED_TO_CHAT_QUEUE:
                event.processing_status = ProcessingStatus.PROCESSING

                return

            if event.with_chat_queue:
                self._set_chat_event_completion(chat_id=event.chat_id)

            self._set_event_completion()

    def _run_event_processing(self) -> None:
        worker_name = threading.current_thread().name
        last_processing_time = time.monotonic()

        while True:
            with self._new_event_condition:
                while not self._events:
                    remaining_secs = (
                        _WORKER_WAITING_SECS
                        - (time.monotonic() - last_processing_time)
                    )

                    if remaining_secs <= 0:
                        with self._worker_lock:
                            if len(self._workers) > self._min_workers:
                                del self._workers[worker_name]
                                logger.debug(
                                    "Worker %r stopped (workers: %r).",
                                    worker_name,
                                    len(self._workers)
                                )

                                return
                            else:
                                remaining_secs = _WORKER_WAITING_SECS

                    self._new_event_condition.wait(timeout=remaining_secs)

                event = self._events.popleft()

            self._process_event(event)
            last_processing_time = time.monotonic()

    def _process_event_error(self, error: Exception, event: EventInfo) -> None:
        # noinspection PyBroadException
        try:
            for i in self._middlewares:
                i.pre_process_error(
                    deps=self._deps,
                    error=error,
                    event=event.event,
                    event_type=event.event_type
                )

            error_handler = self._get_error_handler(error)

            if error_handler is None:
                raise error

            error_handler_context.set(error_handler.handler)

            for i in self._middlewares:
                i.process_error(
                    deps=self._deps,
                    error=error,
                    event=event.event,
                    event_type=event.event_type
                )

            error_handler.handler.process_error(
                deps=self._deps,
                error=error,
                event=event.event
            )

            for i in self._middlewares:
                i.post_process_error(
                    deps=self._deps,
                    error=error,
                    event=event.event,
                    event_type=event.event_type
                )
        except Exception:
            logger.exception("An error occurred while processing an event %r!", event.event)


def _get_event_filter(
    filter_: Optional[AbstractBaseFilter] = None
) -> AbstractBaseFilter:
    return filter_ if filter_ is not None else _none_filter


def _get_server_root(
    update_processor: Callable[[Update], None],
    secret_token: Optional[str] = None
):
    import cherrypy  # noqa

    class ServerRoot:

        def __init__(self):
            self._update_processor = update_processor
            self._secret_token = secret_token
            self._dataclass_converter = Converter()

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
