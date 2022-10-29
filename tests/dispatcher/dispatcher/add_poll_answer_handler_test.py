from unittest.mock import Mock
from typing import Optional

import pytest

from telebox import (
    Dispatcher,
    TelegramBot,
    AbstractEventBaseFilter
)
from telebox.dispatcher.errors import DispatcherError
from tests.dispatcher.dispatcher.helpers import (
    PollAnswerHandler,
    PollAnswerFilter,
    CallbackQueryFilter
)


TEST_FILTER_DATA = (
    ("filter_",),
    (
        (None,),
        (PollAnswerFilter(),),
        (~PollAnswerFilter(),),
        (PollAnswerFilter() & PollAnswerFilter(),),
        (PollAnswerFilter() | PollAnswerFilter(),)
    )
)


@pytest.mark.parametrize(*TEST_FILTER_DATA)
def test(filter_: Optional[AbstractEventBaseFilter], token: str) -> None:
    bot = TelegramBot(session=Mock(), token=token)
    dispatcher = Dispatcher(bot)
    handler = PollAnswerHandler()
    dispatcher.add_poll_answer_handler(handler, filter_)

    assert dispatcher.check_poll_answer_handler(handler, filter_)


def test_unsupported_filter(token: str) -> None:
    bot = TelegramBot(session=Mock(), token=token)
    dispatcher = Dispatcher(bot)
    handler = PollAnswerHandler()
    filter_ = CallbackQueryFilter()

    with pytest.raises(DispatcherError):
        dispatcher.add_poll_answer_handler(handler, filter_)
