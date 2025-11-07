from typing import Union, Optional

from telebox.dispatcher.filters.filter import AbstractFilter
from telebox.dispatcher.types.media_group import MediaGroup
from telebox.bot.types.message import Message
from telebox.bot.types.inline_query import InlineQuery
from telebox.bot.types.chosen_inline_result import ChosenInlineResult
from telebox.bot.types.callback_query import CallbackQuery
from telebox.bot.types.shipping_query import ShippingQuery
from telebox.bot.types.pre_checkout_query import PreCheckoutQuery
from telebox.bot.types.poll_answer import PollAnswer
from telebox.bot.types.chat_member_updated import ChatMemberUpdated
from telebox.bot.types.chat_join_request import ChatJoinRequest
from telebox.bot.types.business_connection import BusinessConnection
from telebox.bot.types.chat_boost_removed import ChatBoostRemoved
from telebox.bot.types.chat_boost_updated import ChatBoostUpdated
from telebox.bot.types.message_reaction_updated import MessageReactionUpdated
from telebox.bot.types.paid_media_purchased import PaidMediaPurchased


class UserFilter(AbstractFilter):
    def __init__(self, *ids: int):
        self._ids = set(ids)

    def get_value(
        self,
        event: Union[
            Message,
            MediaGroup,
            InlineQuery,
            ChosenInlineResult,
            CallbackQuery,
            ShippingQuery,
            PreCheckoutQuery,
            PollAnswer,
            ChatMemberUpdated,
            ChatJoinRequest,
            BusinessConnection,
            ChatBoostRemoved,
            ChatBoostUpdated,
            MessageReactionUpdated,
            PaidMediaPurchased
        ]
    ) -> Optional[int]:
        return event.user_id

    def check_value(self, value: Optional[int]) -> bool:
        if self._ids:
            return value in self._ids

        return value is not None
