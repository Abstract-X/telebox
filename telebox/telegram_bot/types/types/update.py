from dataclasses import dataclass
from typing import Optional

from telebox.typing import UpdateContent
from telebox.telegram_bot.enums.update_content_type import UpdateContentType
from telebox.telegram_bot.errors import UnknownUpdateContentError
from telebox.telegram_bot.types.type import Type
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
    def content(self) -> tuple[UpdateContent, UpdateContentType]:
        if self.message is not None:
            return self.message, UpdateContentType.MESSAGE
        elif self.edited_message is not None:
            return self.edited_message, UpdateContentType.EDITED_MESSAGE
        elif self.channel_post is not None:
            return self.channel_post, UpdateContentType.CHANNEL_POST
        elif self.edited_channel_post is not None:
            return self.edited_channel_post, UpdateContentType.EDITED_CHANNEL_POST
        elif self.inline_query is not None:
            return self.inline_query, UpdateContentType.INLINE_QUERY
        elif self.chosen_inline_result is not None:
            return self.chosen_inline_result, UpdateContentType.CHOSEN_INLINE_RESULT
        elif self.callback_query is not None:
            return self.callback_query, UpdateContentType.CALLBACK_QUERY
        elif self.shipping_query is not None:
            return self.shipping_query, UpdateContentType.SHIPPING_QUERY
        elif self.pre_checkout_query is not None:
            return self.pre_checkout_query, UpdateContentType.PRE_CHECKOUT_QUERY
        elif self.poll is not None:
            return self.poll, UpdateContentType.POLL
        elif self.poll_answer is not None:
            return self.poll_answer, UpdateContentType.POLL_ANSWER
        elif self.my_chat_member is not None:
            return self.my_chat_member, UpdateContentType.MY_CHAT_MEMBER
        elif self.chat_member is not None:
            return self.chat_member, UpdateContentType.CHAT_MEMBER
        elif self.chat_join_request is not None:
            return self.chat_join_request, UpdateContentType.CHAT_JOIN_REQUEST

        raise UnknownUpdateContentError("Unknown update content!")
