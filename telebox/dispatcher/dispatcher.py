import logging
from typing import Optional, Union, Iterable
from threading import Thread
import time

from telebox.telegram_bot.telegram_bot import TelegramBot
from telebox.telegram_bot.types.types.message import Message
from telebox.telegram_bot.types.types.callback_query import CallbackQuery
from telebox.telegram_bot.types.types.chat_member_updated import ChatMemberUpdated
from telebox.telegram_bot.types.types.chat_join_request import ChatJoinRequest
from telebox.dispatcher.utils.thread_pool import ThreadPool
from telebox.dispatcher.utils.event_queue import EventQueue, Item
from telebox.dispatcher.enums.event_type import EventType
from telebox.dispatcher.handlers.event import AbstractEventHandler
from telebox.dispatcher.handlers.error import AbstractErrorHandler
from telebox.dispatcher.filters.base.event import AbstractEventFilter
from telebox.dispatcher.filters.base.error import AbstractErrorFilter
from telebox.utils import RequestTimeout
from telebox.typing import Event
from telebox.dispatcher.errors import PollingAlreadyStartedError


logger = logging.getLogger(__name__)
EventHandlerDict = dict[
    EventType,
    list[
        tuple[
            AbstractEventHandler,
            tuple[AbstractEventFilter, ...]
        ]
    ]
]
ErrorHandlerList = list[
    tuple[
        AbstractErrorHandler,
        tuple[AbstractErrorFilter, ...]
    ]
]


class Dispatcher:

    def __init__(self, bot: TelegramBot):
        self._bot = bot
        self._polling_is_started = False
        self._event_handlers: EventHandlerDict = {i: [] for i in EventType}
        self._error_handlers: ErrorHandlerList = []

    def add_event_handler(
        self,
        handler: AbstractEventHandler,
        event_type: EventType,
        filters: Iterable[AbstractEventFilter] = ()
    ) -> None:
        self._event_handlers[event_type].append((handler, tuple(filters)))

    def add_message_handler(
        self,
        handler: AbstractEventHandler,
        filters: Iterable[AbstractEventFilter] = ()
    ) -> None:
        self.add_event_handler(handler, EventType.MESSAGE, filters)

    def add_edited_message_handler(
        self,
        handler: AbstractEventHandler,
        filters: Iterable[AbstractEventFilter] = ()
    ) -> None:
        self.add_event_handler(handler, EventType.EDITED_MESSAGE, filters)

    def add_channel_post_handler(
        self,
        handler: AbstractEventHandler,
        filters: Iterable[AbstractEventFilter] = ()
    ) -> None:
        self.add_event_handler(handler, EventType.CHANNEL_POST, filters)

    def add_edited_channel_post_handler(
        self,
        handler: AbstractEventHandler,
        filters: Iterable[AbstractEventFilter] = ()
    ) -> None:
        self.add_event_handler(handler, EventType.EDITED_CHANNEL_POST, filters)

    def add_inline_query_handler(
        self,
        handler: AbstractEventHandler,
        filters: Iterable[AbstractEventFilter] = ()
    ) -> None:
        self.add_event_handler(handler, EventType.INLINE_QUERY, filters)

    def add_chosen_inline_result_handler(
        self,
        handler: AbstractEventHandler,
        filters: Iterable[AbstractEventFilter] = ()
    ) -> None:
        self.add_event_handler(handler, EventType.CHOSEN_INLINE_RESULT, filters)

    def add_callback_query_handler(
        self,
        handler: AbstractEventHandler,
        filters: Iterable[AbstractEventFilter] = ()
    ) -> None:
        self.add_event_handler(handler, EventType.CALLBACK_QUERY, filters)

    def add_shipping_query_handler(
        self,
        handler: AbstractEventHandler,
        filters: Iterable[AbstractEventFilter] = ()
    ) -> None:
        self.add_event_handler(handler, EventType.SHIPPING_QUERY, filters)

    def add_pre_checkout_query_handler(
        self,
        handler: AbstractEventHandler,
        filters: Iterable[AbstractEventFilter] = ()
    ) -> None:
        self.add_event_handler(handler, EventType.PRE_CHECKOUT_QUERY, filters)

    def add_poll_handler(
        self,
        handler: AbstractEventHandler,
        filters: Iterable[AbstractEventFilter] = ()
    ) -> None:
        self.add_event_handler(handler, EventType.POLL, filters)

    def add_poll_answer_handler(
        self,
        handler: AbstractEventHandler,
        filters: Iterable[AbstractEventFilter] = ()
    ) -> None:
        self.add_event_handler(handler, EventType.POLL_ANSWER, filters)

    def add_my_chat_member_handler(
        self,
        handler: AbstractEventHandler,
        filters: Iterable[AbstractEventFilter] = ()
    ) -> None:
        self.add_event_handler(handler, EventType.MY_CHAT_MEMBER, filters)

    def add_chat_member_handler(
        self,
        handler: AbstractEventHandler,
        filters: Iterable[AbstractEventFilter] = ()
    ) -> None:
        self.add_event_handler(handler, EventType.CHAT_MEMBER, filters)

    def add_chat_join_request_handler(
        self,
        handler: AbstractEventHandler,
        filters: Iterable[AbstractEventFilter] = ()
    ) -> None:
        self.add_event_handler(handler, EventType.CHAT_JOIN_REQUEST, filters)

    def add_error_handler(
        self,
        handler: AbstractErrorHandler,
        filters: Iterable[AbstractErrorFilter] = ()
    ) -> None:
        self._error_handlers.append((handler, tuple(filters)))

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
        event_queue = EventQueue()
        delayed_event_processing_thread = Thread(
            target=event_queue.run_delayed_event_processing,
            daemon=True
        )
        delayed_event_processing_thread.start()
        thread_pool = ThreadPool(
            threads=threads,
            target=self._run_event_queue_processing,
            args=(event_queue,)
        )
        thread_pool.start()

        try:
            logger.info("Polling started.")

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
                    if updates:
                        offset_update_id = updates[-1].update_id + 1

                        for i in updates:
                            logger.debug("Update received: %r.", i)
                            event, event_type = i.content
                            item = Item(
                                event=event,
                                event_type=event_type,
                                chat_id=_get_event_chat_id(event)
                            )
                            event_queue.add_item(item)

                    time.sleep(delay_secs)
        except KeyboardInterrupt:
            logger.info("Polling stopped.")
            logger.info("Finishing processing updates...", )
            event_queue.wait_processing()
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

    def _run_event_queue_processing(self, queue: EventQueue) -> None:
        while True:
            item = queue.get_item()

            try:
                logger.debug("Event processing started: %r.", item.event)
                event_handler = self._get_event_handler(item.event, item.event_type)

                if event_handler is not None:
                    # noinspection PyBroadException
                    try:
                        try:
                            event_handler.process(item.event)
                        except Exception as error:
                            error_handler = self._get_error_handler(error, item.event)

                            if error_handler is None:
                                raise

                            error_handler.process(error, item.event)
                    except Exception:
                        logger.exception("An error occurred while processing an update!")
            finally:
                queue.notify_about_processed_item(item)
                logger.debug("Event processing finished: %r.", item.event)

    def _get_event_handler(
        self,
        event: Event,
        event_type: EventType
    ) -> Optional[AbstractEventHandler]:
        return _get_handler(self._event_handlers[event_type], (event,))

    def _get_error_handler(
        self,
        error: Exception,
        event: Event
    ) -> Optional[AbstractErrorHandler]:
        return _get_handler(self._error_handlers, (error, event))


def _get_handler(handlers: list[tuple], check_args: tuple):
    filter_results = {}

    for handler, filters in handlers:
        for filter_ in filters:
            try:
                result = filter_results[filter_]
            except KeyError:
                result = filter_results[filter_] = filter_.check(*check_args)

            if not result:
                break
        else:
            return handler


def _get_event_chat_id(event: Event) -> Optional[int]:
    if isinstance(event, (Message, CallbackQuery, ChatMemberUpdated, ChatJoinRequest)):
        return event.chat_id
