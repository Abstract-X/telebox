from unittest.mock import Mock
from typing import Optional

import pytest

from telebox import Dispatcher, TelegramBot, AbstractErrorBaseFilter
from tests.dispatcher.dispatcher.helpers import ErrorHandler, ErrorFilter


TEST_FILTER_DATA = (
    ("filter_",),
    (
        (None,),
        (ErrorFilter(),),
        (~ErrorFilter(),),
        (ErrorFilter() & ErrorFilter(),),
        (ErrorFilter() | ErrorFilter(),)
    )
)


@pytest.mark.parametrize(*TEST_FILTER_DATA)
def test(filter_: Optional[AbstractErrorBaseFilter], token: str) -> None:
    bot = TelegramBot(session=Mock(), token=token)
    dispatcher = Dispatcher(bot)
    handler = ErrorHandler()
    dispatcher.add_error_handler(handler, filter_)

    assert dispatcher.check_error_handler(handler, filter_)
