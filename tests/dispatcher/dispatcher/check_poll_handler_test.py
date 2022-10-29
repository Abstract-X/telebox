from unittest.mock import Mock
from typing import Optional

import pytest

from telebox import Dispatcher, TelegramBot, AbstractEventBaseFilter
from tests.dispatcher.dispatcher.helpers import PollHandler, PollFilter


TEST_FILTER_DATA = (
    ("filter_",),
    (
        (None,),
        (PollFilter(),),
        (~PollFilter(),),
        (PollFilter() & PollFilter(),),
        (PollFilter() | PollFilter(),)
    )
)


@pytest.mark.parametrize(*TEST_FILTER_DATA)
def test(filter_: Optional[AbstractEventBaseFilter], token: str) -> None:
    bot = TelegramBot(session=Mock(), token=token)
    dispatcher = Dispatcher(bot)
    handler = PollHandler()

    assert dispatcher.check_poll_handler(handler, filter_) is False

    dispatcher.add_poll_handler(handler, filter_)

    assert dispatcher.check_poll_handler(handler, filter_) is True
