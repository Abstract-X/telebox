from typing import Union

from telebox.dispatcher.filters.base.event import AbstractEventFilter
from telebox.telegram_bot.types.types.message import Message
from telebox.telegram_bot.types.types.inline_query import InlineQuery
from telebox.telegram_bot.types.types.chosen_inline_result import ChosenInlineResult
from telebox.telegram_bot.types.types.callback_query import CallbackQuery
from telebox.telegram_bot.types.types.shipping_query import ShippingQuery
from telebox.telegram_bot.types.types.pre_checkout_query import PreCheckoutQuery
from telebox.telegram_bot.types.types.poll_answer import PollAnswer
from telebox.telegram_bot.types.types.chat_member_updated import ChatMemberUpdated
from telebox.telegram_bot.types.types.chat_join_request import ChatJoinRequest


class UserIDFilter(AbstractEventFilter):

    def __init__(self, *ids: int):
        self._ids = set(ids)

    def check(
        self,
        event: Union[
            Message,
            InlineQuery,
            ChosenInlineResult,
            CallbackQuery,
            ShippingQuery,
            PreCheckoutQuery,
            PollAnswer,
            ChatMemberUpdated,
            ChatJoinRequest
        ]
    ) -> bool:
        if isinstance(
            event, (
                Message,
                InlineQuery,
                ChosenInlineResult,
                CallbackQuery,
                ShippingQuery,
                PreCheckoutQuery,
                ChatMemberUpdated,
                ChatJoinRequest
            )
        ):
            return event.from_.id in self._ids
        elif isinstance(event, PollAnswer):
            return event.user.id in self._ids

        return False
