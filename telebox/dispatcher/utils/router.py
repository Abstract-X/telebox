from __future__ import annotations
from typing import Optional, Union, TYPE_CHECKING

if TYPE_CHECKING:
    from telebox.dispatcher.dispatcher import Dispatcher
from telebox.dispatcher.handlers.event import AbstractEventHandler
from telebox.dispatcher.filters.events.filter import AbstractEventBaseFilter
from telebox.dispatcher.utils.rate_limiter.rate_limit import RateLimit
from telebox.utils.not_set import NotSet, NOT_SET


class Router:

    def __init__(
        self,
        dispatcher: Dispatcher,
        filter_: Optional[AbstractEventBaseFilter] = None
    ):
        self._dispatcher = dispatcher
        self.filter = filter_

    def __add__(self, other: Union[AbstractEventBaseFilter, Router]) -> Router:
        if isinstance(other, AbstractEventBaseFilter):
            return Router(self._dispatcher, self._get_filter(other))
        elif isinstance(other, Router):
            return Router(self._dispatcher, self._get_filter(other.filter))

        return NotImplemented

    def __iadd__(self, other: Union[AbstractEventBaseFilter, Router]) -> Router:
        return self.__add__(other)

    def add_message_handler(
        self,
        handler: AbstractEventHandler,
        filter_: Optional[AbstractEventBaseFilter] = None,
        rate_limit: Union[RateLimit, None, NotSet] = NOT_SET,
        with_chat_waiting: bool = True
    ) -> None:
        self._dispatcher.add_message_handler(
            handler=handler,
            filter_=self._get_filter(filter_),
            rate_limit=rate_limit,
            with_chat_waiting=with_chat_waiting
        )

    def add_edited_message_handler(
        self,
        handler: AbstractEventHandler,
        filter_: Optional[AbstractEventBaseFilter] = None,
        rate_limit: Union[RateLimit, None, NotSet] = NOT_SET,
        with_chat_waiting: bool = False
    ) -> None:
        self._dispatcher.add_edited_message_handler(
            handler=handler,
            filter_=self._get_filter(filter_),
            rate_limit=rate_limit,
            with_chat_waiting=with_chat_waiting
        )

    def add_channel_post_handler(
        self,
        handler: AbstractEventHandler,
        filter_: Optional[AbstractEventBaseFilter] = None,
        rate_limit: Union[RateLimit, None, NotSet] = NOT_SET,
        with_chat_waiting: bool = False
    ) -> None:
        self._dispatcher.add_channel_post_handler(
            handler=handler,
            filter_=self._get_filter(filter_),
            rate_limit=rate_limit,
            with_chat_waiting=with_chat_waiting
        )

    def add_edited_channel_post_handler(
        self,
        handler: AbstractEventHandler,
        filter_: Optional[AbstractEventBaseFilter] = None,
        rate_limit: Union[RateLimit, None, NotSet] = NOT_SET,
        with_chat_waiting: bool = False
    ) -> None:
        self._dispatcher.add_edited_channel_post_handler(
            handler=handler,
            filter_=self._get_filter(filter_),
            rate_limit=rate_limit,
            with_chat_waiting=with_chat_waiting
        )

    def add_media_group_handler(
        self,
        handler: AbstractEventHandler,
        filter_: Optional[AbstractEventBaseFilter] = None,
        rate_limit: Union[RateLimit, None, NotSet] = NOT_SET,
        with_chat_waiting: bool = True
    ) -> None:
        self._dispatcher.add_media_group_handler(
            handler=handler,
            filter_=self._get_filter(filter_),
            rate_limit=rate_limit,
            with_chat_waiting=with_chat_waiting
        )

    def add_channel_media_group_handler(
        self,
        handler: AbstractEventHandler,
        filter_: Optional[AbstractEventBaseFilter] = None,
        rate_limit: Union[RateLimit, None, NotSet] = NOT_SET,
        with_chat_waiting: bool = False
    ) -> None:
        self._dispatcher.add_channel_media_group_handler(
            handler=handler,
            filter_=self._get_filter(filter_),
            rate_limit=rate_limit,
            with_chat_waiting=with_chat_waiting
        )

    def add_inline_query_handler(
        self,
        handler: AbstractEventHandler,
        filter_: Optional[AbstractEventBaseFilter] = None,
        rate_limit: Union[RateLimit, None, NotSet] = NOT_SET
    ) -> None:
        self._dispatcher.add_inline_query_handler(
            handler=handler,
            filter_=self._get_filter(filter_),
            rate_limit=rate_limit
        )

    def add_chosen_inline_result_handler(
        self,
        handler: AbstractEventHandler,
        filter_: Optional[AbstractEventBaseFilter] = None,
        rate_limit: Union[RateLimit, None, NotSet] = NOT_SET
    ) -> None:
        self._dispatcher.add_chosen_inline_result_handler(
            handler=handler,
            filter_=self._get_filter(filter_),
            rate_limit=rate_limit
        )

    def add_callback_query_handler(
        self,
        handler: AbstractEventHandler,
        filter_: Optional[AbstractEventBaseFilter] = None,
        rate_limit: Union[RateLimit, None, NotSet] = NOT_SET,
        with_chat_waiting: bool = True
    ) -> None:
        self._dispatcher.add_callback_query_handler(
            handler=handler,
            filter_=self._get_filter(filter_),
            rate_limit=rate_limit,
            with_chat_waiting=with_chat_waiting
        )

    def add_shipping_query_handler(
        self,
        handler: AbstractEventHandler,
        filter_: Optional[AbstractEventBaseFilter] = None,
        rate_limit: Union[RateLimit, None, NotSet] = NOT_SET
    ) -> None:
        self._dispatcher.add_shipping_query_handler(
            handler=handler,
            filter_=self._get_filter(filter_),
            rate_limit=rate_limit
        )

    def add_pre_checkout_query_handler(
        self,
        handler: AbstractEventHandler,
        filter_: Optional[AbstractEventBaseFilter] = None,
        rate_limit: Union[RateLimit, None, NotSet] = NOT_SET
    ) -> None:
        self._dispatcher.add_pre_checkout_query_handler(
            handler=handler,
            filter_=self._get_filter(filter_),
            rate_limit=rate_limit
        )

    def add_poll_handler(
        self,
        handler: AbstractEventHandler,
        filter_: Optional[AbstractEventBaseFilter] = None
    ) -> None:
        self._dispatcher.add_poll_handler(
            handler=handler,
            filter_=self._get_filter(filter_)
        )

    def add_poll_answer_handler(
        self,
        handler: AbstractEventHandler,
        filter_: Optional[AbstractEventBaseFilter] = None
    ) -> None:
        self._dispatcher.add_poll_answer_handler(
            handler=handler,
            filter_=self._get_filter(filter_)
        )

    def add_my_chat_member_handler(
        self,
        handler: AbstractEventHandler,
        filter_: Optional[AbstractEventBaseFilter] = None,
        with_chat_waiting: bool = False
    ) -> None:
        self._dispatcher.add_my_chat_member_handler(
            handler=handler,
            filter_=self._get_filter(filter_),
            with_chat_waiting=with_chat_waiting
        )

    def add_chat_member_handler(
        self,
        handler: AbstractEventHandler,
        filter_: Optional[AbstractEventBaseFilter] = None,
        with_chat_waiting: bool = False
    ) -> None:
        self._dispatcher.add_chat_member_handler(
            handler=handler,
            filter_=self._get_filter(filter_),
            with_chat_waiting=with_chat_waiting
        )

    def add_chat_join_request_handler(
        self,
        handler: AbstractEventHandler,
        filter_: Optional[AbstractEventBaseFilter] = None
    ) -> None:
        self._dispatcher.add_chat_join_request_handler(
            handler=handler,
            filter_=self._get_filter(filter_)
        )

    def _get_filter(self, filter_: AbstractEventBaseFilter) -> Optional[AbstractEventBaseFilter]:
        if filter_ is None:
            return self.filter
        elif self.filter is None:
            return filter_

        return self.filter & filter_
