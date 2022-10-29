from unittest.mock import Mock
from typing import Optional, Union

import pytest

from telebox import (
    Dispatcher,
    TelegramBot,
    AbstractEventBaseFilter,
    RateLimit,
    Limit,
    NotSet,
    NOT_SET
)
from telebox.dispatcher.errors import DispatcherError
from tests.dispatcher.dispatcher.helpers import (
    InlineQueryHandler,
    InlineQueryFilter,
    CallbackQueryFilter
)


TEST_FILTER_DATA = (
    ("filter_",),
    (
        (None,),
        (InlineQueryFilter(),),
        (~InlineQueryFilter(),),
        (InlineQueryFilter() & InlineQueryFilter(),),
        (InlineQueryFilter() | InlineQueryFilter(),)
    )
)
TEST_RATE_LIMIT_DATA = (
    ("rate_limit",),
    (
        (NOT_SET,),
        (None,),
        (RateLimit(user_limit=Limit(1, 1)),)
    )
)


@pytest.mark.parametrize(*TEST_FILTER_DATA)
@pytest.mark.parametrize(*TEST_RATE_LIMIT_DATA)
def test(
    filter_: Optional[AbstractEventBaseFilter],
    rate_limit: Union[RateLimit, None, NotSet],
    token: str
) -> None:
    bot = TelegramBot(session=Mock(), token=token)
    dispatcher = Dispatcher(bot)
    handler = InlineQueryHandler()
    dispatcher.add_inline_query_handler(handler, filter_, rate_limit)

    assert dispatcher.check_inline_query_handler(handler, filter_, rate_limit)


def test_unsupported_filter(token: str) -> None:
    bot = TelegramBot(session=Mock(), token=token)
    dispatcher = Dispatcher(bot)
    handler = InlineQueryHandler()
    filter_ = CallbackQueryFilter()

    with pytest.raises(DispatcherError):
        dispatcher.add_inline_query_handler(handler, filter_)


def test_default_rate_limit(token: str) -> None:
    bot = TelegramBot(session=Mock(), token=token)
    rate_limit = RateLimit(user_limit=Limit(1, 1))
    dispatcher = Dispatcher(bot, default_rate_limit=rate_limit)
    handler = InlineQueryHandler()
    filter_ = InlineQueryFilter()
    dispatcher.add_inline_query_handler(handler, filter_)

    assert dispatcher.check_inline_query_handler(handler, filter_, rate_limit)
