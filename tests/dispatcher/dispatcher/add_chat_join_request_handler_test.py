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
    ChatJoinRequestHandler,
    ChatJoinRequestFilter,
    CallbackQueryFilter
)


TEST_FILTER_DATA = (
    ("filter_",),
    (
        (None,),
        (ChatJoinRequestFilter(),),
        (~ChatJoinRequestFilter(),),
        (ChatJoinRequestFilter() & ChatJoinRequestFilter(),),
        (ChatJoinRequestFilter() | ChatJoinRequestFilter(),)
    )
)


@pytest.mark.parametrize(*TEST_FILTER_DATA)
def test(filter_: Optional[AbstractEventBaseFilter], token: str) -> None:
    bot = TelegramBot(session=Mock(), token=token)
    dispatcher = Dispatcher(bot)
    handler = ChatJoinRequestHandler()
    dispatcher.add_chat_join_request_handler(handler, filter_)

    assert dispatcher.check_chat_join_request_handler(handler, filter_)


def test_unsupported_filter(token: str) -> None:
    bot = TelegramBot(session=Mock(), token=token)
    dispatcher = Dispatcher(bot)
    handler = ChatJoinRequestHandler()
    filter_ = CallbackQueryFilter()

    with pytest.raises(DispatcherError):
        dispatcher.add_chat_join_request_handler(handler, filter_)
