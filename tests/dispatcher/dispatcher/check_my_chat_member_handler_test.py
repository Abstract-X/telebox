from unittest.mock import Mock
from typing import Optional

import pytest

from telebox import Dispatcher, TelegramBot, AbstractEventBaseFilter
from tests.dispatcher.dispatcher.helpers import MyChatMemberHandler, MyChatMemberFilter


TEST_FILTER_DATA = (
    ("filter_",),
    (
        (None,),
        (MyChatMemberFilter(),),
        (~MyChatMemberFilter(),),
        (MyChatMemberFilter() & MyChatMemberFilter(),),
        (MyChatMemberFilter() | MyChatMemberFilter(),)
    )
)


@pytest.mark.parametrize(*TEST_FILTER_DATA)
def test(filter_: Optional[AbstractEventBaseFilter], token: str) -> None:
    bot = TelegramBot(session=Mock(), token=token)
    dispatcher = Dispatcher(bot)
    handler = MyChatMemberHandler()

    assert dispatcher.check_my_chat_member_handler(handler, filter_) is False

    dispatcher.add_my_chat_member_handler(handler, filter_)

    assert dispatcher.check_my_chat_member_handler(handler, filter_) is True
