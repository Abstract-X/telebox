from dataclasses import dataclass
from typing import Optional, Union

from telebox.bot.enums.update_content_type import UpdateContentType
from telebox.bot.types.type import Type
from telebox.bot.types.types.message import Message
from telebox.bot.types.types.inline_query import InlineQuery
from telebox.bot.types.types.chosen_inline_result import ChosenInlineResult
from telebox.bot.types.types.callback_query import CallbackQuery
from telebox.bot.types.types.shipping_query import ShippingQuery
from telebox.bot.types.types.pre_checkout_query import PreCheckoutQuery
from telebox.bot.types.types.poll import Poll
from telebox.bot.types.types.poll_answer import PollAnswer
from telebox.bot.types.types.chat_member_updated import ChatMemberUpdated
from telebox.bot.types.types.chat_join_request import ChatJoinRequest


UpdateContent = Union[
    Message,
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


@dataclass(eq=False)
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

    def __post_init__(self) -> None:
        if self.message is not None:
            self._content = self.message
            self._content_type = UpdateContentType.MESSAGE
        elif self.edited_message is not None:
            self._content = self.edited_message
            self._content_type = UpdateContentType.EDITED_MESSAGE
        elif self.channel_post is not None:
            self._content = self.channel_post
            self._content_type = UpdateContentType.CHANNEL_POST
        elif self.edited_channel_post is not None:
            self._content = self.edited_channel_post
            self._content_type = UpdateContentType.EDITED_CHANNEL_POST
        elif self.inline_query is not None:
            self._content = self.inline_query
            self._content_type = UpdateContentType.INLINE_QUERY
        elif self.chosen_inline_result is not None:
            self._content = self.chosen_inline_result
            self._content_type = UpdateContentType.CHOSEN_INLINE_RESULT
        elif self.callback_query is not None:
            self._content = self.callback_query
            self._content_type = UpdateContentType.CALLBACK_QUERY
        elif self.shipping_query is not None:
            self._content = self.shipping_query
            self._content_type = UpdateContentType.SHIPPING_QUERY
        elif self.pre_checkout_query is not None:
            self._content = self.pre_checkout_query
            self._content_type = UpdateContentType.PRE_CHECKOUT_QUERY
        elif self.poll is not None:
            self._content = self.poll
            self._content_type = UpdateContentType.POLL
        elif self.poll_answer is not None:
            self._content = self.poll_answer
            self._content_type = UpdateContentType.POLL_ANSWER
        elif self.my_chat_member is not None:
            self._content = self.my_chat_member
            self._content_type = UpdateContentType.MY_CHAT_MEMBER
        elif self.chat_member is not None:
            self._content = self.chat_member
            self._content_type = UpdateContentType.CHAT_MEMBER
        elif self.chat_join_request is not None:
            self._content = self.chat_join_request
            self._content_type = UpdateContentType.CHAT_JOIN_REQUEST
        else:
            self._content = self._content_type = None

    @property
    def content(self) -> Optional[UpdateContent]:
        return self._content

    @property
    def content_type(self) -> Optional[UpdateContentType]:
        return self._content_type
