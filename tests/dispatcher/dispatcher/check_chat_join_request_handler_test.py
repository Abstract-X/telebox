from unittest.mock import Mock
from typing import Optional

import pytest

from telebox import Dispatcher, TelegramBot, AbstractEventBaseFilter
from tests.dispatcher.dispatcher.helpers import ChatJoinRequestHandler, ChatJoinRequestFilter


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

    assert dispatcher.check_chat_join_request_handler(handler, filter_) is False

    dispatcher.add_chat_join_request_handler(handler, filter_)

    assert dispatcher.check_chat_join_request_handler(handler, filter_) is True
