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
from tests.dispatcher.dispatcher.helpers import ShippingQueryHandler, ShippingQueryFilter


TEST_FILTER_DATA = (
    ("filter_",),
    (
        (None,),
        (ShippingQueryFilter(),),
        (~ShippingQueryFilter(),),
        (ShippingQueryFilter() & ShippingQueryFilter(),),
        (ShippingQueryFilter() | ShippingQueryFilter(),)
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
    handler = ShippingQueryHandler()

    assert dispatcher.check_shipping_query_handler(handler, filter_, rate_limit) is False

    dispatcher.add_shipping_query_handler(handler, filter_, rate_limit)

    assert dispatcher.check_shipping_query_handler(handler, filter_, rate_limit) is True


def test_default_rate_limit(token: str) -> None:
    bot = TelegramBot(session=Mock(), token=token)
    rate_limit = RateLimit(user_limit=Limit(1, 1))
    dispatcher = Dispatcher(bot, default_rate_limit=rate_limit)
    handler = ShippingQueryHandler()
    filter_ = ShippingQueryFilter()

    assert dispatcher.check_shipping_query_handler(handler, filter_, rate_limit) is False

    dispatcher.add_shipping_query_handler(handler, filter_)

    assert dispatcher.check_shipping_query_handler(handler, filter_, rate_limit) is True
