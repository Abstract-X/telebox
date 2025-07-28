from typing import Union

from telebox.bot.types.message import Message
from telebox.bot.types.inline_query import InlineQuery
from telebox.bot.types.chosen_inline_result import ChosenInlineResult
from telebox.bot.types.callback_query import CallbackQuery
from telebox.bot.types.shipping_query import ShippingQuery
from telebox.bot.types.pre_checkout_query import PreCheckoutQuery
from telebox.bot.types.poll import Poll
from telebox.bot.types.poll_answer import PollAnswer
from telebox.bot.types.chat_member_updated import ChatMemberUpdated
from telebox.bot.types.chat_join_request import ChatJoinRequest
from telebox.dispatcher.utils.media_group import MediaGroup


Event = Union[
    Message,
    MediaGroup,
    InlineQuery,
    ChosenInlineResult,
    CallbackQuery,
    ShippingQuery,
    PreCheckoutQuery,
    Poll,
    PollAnswer,
    ChatMemberUpdated,
    ChatJoinRequest
]
