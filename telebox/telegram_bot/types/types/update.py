from dataclasses import dataclass
from typing import Optional

from telebox.telegram_bot.types.base import Type
from telebox.telegram_bot.types.types.message import Message
from telebox.telegram_bot.types.types.inline_query import InlineQuery
from telebox.telegram_bot.types.types.chosen_inline_result import ChosenInlineResult
from telebox.telegram_bot.types.types.callback_query import CallbackQuery
from telebox.telegram_bot.types.types.shipping_query import ShippingQuery
from telebox.telegram_bot.types.types.pre_checkout_query import PreCheckoutQuery
from telebox.telegram_bot.types.types.poll import Poll
from telebox.telegram_bot.types.types.poll_answer import PollAnswer
from telebox.telegram_bot.types.types.chat_member_updated import ChatMemberUpdated
from telebox.telegram_bot.types.types.chat_join_request import ChatJoinRequest
from telebox.telegram_bot.enums.update_type import UpdateType
from telebox.telegram_bot.errors import UnknownUpdateTypeError


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

    @property
    def type(self) -> UpdateType:
        if self.message is not None:
            return UpdateType.MESSAGE
        elif self.edited_message is not None:
            return UpdateType.EDITED_MESSAGE
        elif self.channel_post is not None:
            return UpdateType.CHANNEL_POST
        elif self.edited_channel_post is not None:
            return UpdateType.EDITED_CHANNEL_POST
        elif self.inline_query is not None:
            return UpdateType.INLINE_QUERY
        elif self.chosen_inline_result is not None:
            return UpdateType.CHOSEN_INLINE_RESULT
        elif self.callback_query is not None:
            return UpdateType.CALLBACK_QUERY
        elif self.shipping_query is not None:
            return UpdateType.SHIPPING_QUERY
        elif self.pre_checkout_query is not None:
            return UpdateType.PRE_CHECKOUT_QUERY
        elif self.poll is not None:
            return UpdateType.POLL
        elif self.poll_answer is not None:
            return UpdateType.POLL_ANSWER
        elif self.my_chat_member is not None:
            return UpdateType.MY_CHAT_MEMBER
        elif self.chat_member is not None:
            return UpdateType.CHAT_MEMBER
        elif self.chat_join_request is not None:
            return UpdateType.CHAT_JOIN_REQUEST

        raise UnknownUpdateTypeError("Unknown update type!")
