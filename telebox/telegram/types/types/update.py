from dataclasses import dataclass
from typing import Optional

from telebox.telegram.types.base import Type
from telebox.telegram.types.types.message import Message
from telebox.telegram.types.types.inline_query import InlineQuery
from telebox.telegram.types.types.chosen_inline_result import ChosenInlineResult
from telebox.telegram.types.types.callback_query import CallbackQuery
from telebox.telegram.types.types.shipping_query import ShippingQuery
from telebox.telegram.types.types.pre_checkout_query import PreCheckoutQuery
from telebox.telegram.types.types.poll import Poll
from telebox.telegram.types.types.poll_answer import PollAnswer
from telebox.telegram.types.types.chat_member_updated import ChatMemberUpdated
from telebox.telegram.types.types.chat_join_request import ChatJoinRequest


@dataclass(unsafe_hash=True)
class Update(Type):
    update_id: int
    message: Optional[Message] = None
    edited_message: Optional[Message] = None
    channel_post: Optional[Message] = None
    edited_channel_post: Optional[Message] = None
    inline_query: Optional[InlineQuery] = None
    chosen_inline_result: Optional[ChosenInlineResult] = None
    callback_query: Optional[CallbackQuery] = None
    shipping_query: Optional[ShippingQuery] = None
    pre_checkout_query: Optional[PreCheckoutQuery] = None
    poll: Optional[Poll] = None
    poll_answer: Optional[PollAnswer] = None
    my_chat_member: Optional[ChatMemberUpdated] = None
    chat_member: Optional[ChatMemberUpdated] = None
    chat_join_request: Optional[ChatJoinRequest] = None
